#![allow(clippy::manual_strip, clippy::unnecessary_wraps)] // suppress warnings in py_fn! macro
use cfg_if::cfg_if;
use cpython::exc::{IOError, ValueError};
use cpython::{PyErr, PyObject, PyResult, Python};
use mio::net::{TcpListener, UnixListener};
use std::time::Duration;

use crate::filewrapper::FileWrapper;
use crate::globals::{shared_wsgi_options, ServerOptions};
use crate::pyutils::{async_logger, sync_logger};
use crate::server::Server;
use crate::startresponse::StartResponse;
use crate::transport::{parse_server_info, shared_connection_options};

#[cfg(target_os = "linux")]
use crate::transport::SocketActivation;

macro_rules! server_loop {
    ($L:ty, $application: ident, $listener: ident, $server_options: ident, $async_logging: ident, $py: ident) => {
        match Server::<$L>::new($application, $listener, $server_options, $py) {
            Ok(mut server) => {
                let res = if $async_logging {
                    async_logger($py, "pyruvate")
                } else {
                    sync_logger($py, "pyruvate")
                };
                match res {
                    Ok(_) => match server.serve() {
                        Ok(_) => Ok($py.None()),
                        Err(_) => Err(PyErr::new::<IOError, _>(
                            $py,
                            "Error encountered during event loop",
                        )),
                    },
                    Err(_) => Err(PyErr::new::<IOError, _>($py, "Could not setup logging")),
                }
            }
            Err(e) => Err(PyErr::new::<IOError, _>(
                $py,
                format!("Could not create server: {e:?}"),
            )),
        }
    };
}

#[allow(clippy::too_many_arguments)]
pub fn serve(
    py: Python,
    application: PyObject,
    addr: Option<String>,
    num_workers: usize,
    max_number_headers: usize,
    async_logging: bool,
    chunked_transfer: bool,
    max_reuse_count: u8,
    keepalive_timeout: u8,
    qmon_warn_threshold: Option<usize>,
    send_timeout: u8,
) -> PyResult<PyObject> {
    if num_workers < 1 {
        return Err(PyErr::new::<ValueError, _>(py, "Need at least 1 worker"));
    }
    // addr can be a TCP or Unix domain socket address
    // or None when using a systemd socket.
    let (sockaddr, server_name, server_port) = parse_server_info(addr.clone());
    let server_options = ServerOptions {
        num_workers,
        max_number_headers,
        connection_options: shared_connection_options(
            max_reuse_count,
            Duration::from_secs(keepalive_timeout.into()),
        ),
        wsgi_options: shared_wsgi_options(
            server_name.clone(),
            server_port,
            String::new(),
            chunked_transfer,
            qmon_warn_threshold,
            Duration::from_secs(send_timeout.into()),
            py,
        ),
    };
    match addr {
        Some(_) => {
            match sockaddr {
                Some(sockaddr) => match TcpListener::bind(sockaddr) {
                    Ok(listener) => server_loop!(
                        TcpListener,
                        application,
                        listener,
                        server_options,
                        async_logging,
                        py
                    ),
                    Err(e) => Err(PyErr::new::<IOError, _>(
                        py,
                        format!("Could not bind socket: {e:?}"),
                    )),
                },
                None => {
                    // fallback to UnixListener
                    match UnixListener::bind(server_name) {
                        Ok(listener) => server_loop!(
                            UnixListener,
                            application,
                            listener,
                            server_options,
                            async_logging,
                            py
                        ),
                        Err(e) => Err(PyErr::new::<IOError, _>(
                            py,
                            format!("Could not bind unix domain socket: {e:?}"),
                        )),
                    }
                }
            }
        }
        None => {
            cfg_if! {
                if #[cfg(target_os = "linux")] {
                    // try systemd socket activation
                    match TcpListener::from_active_socket() {
                        Ok(listener) => server_loop!(
                            TcpListener,
                            application,
                            listener,
                            server_options,
                            async_logging,
                            py
                        ),
                        Err(_) => {
                            // fall back to UnixListener
                            match UnixListener::from_active_socket() {
                                Ok(listener) => server_loop!(
                                    UnixListener,
                                    application,
                                    listener,
                                    server_options,
                                    async_logging,
                                    py
                                ),
                                Err(e) => Err(PyErr::new::<IOError, _>(
                                    py,
                                    format!("Socket activation: {e}"),
                                )),
                            }
                        }
                    }
                } else {
                    Err(PyErr::new::<IOError, _>(
                        py,
                        "Could not bind socket.",
                    ))
                }
            }
        }
    }
}

py_module_initializer!(pyruvate, initpyruvate, PyInit_pyruvate, |py, m| {
    m.add(py, "__doc__", "Pyruvate WSGI server")
        .expect("Could not add documentation string");
    m.add_class::<StartResponse>(py)
        .expect("Could not add StartResponse class to module");
    m.add_class::<FileWrapper>(py)
        .expect("Could not add FileWrapper class to module");
    m.add(
        py,
        "serve",
        py_fn!(
            py,
            serve(
                application: PyObject,
                addr: Option<String> = None,
                num_workers: usize = 2,
                max_number_headers: usize = 32,
                async_logging: bool = true,
                chunked_transfer: bool = false,
                max_reuse_count: u8 = 0,
                keepalive_timeout: u8 = 60,
                qmon_warn_threshold: Option<usize> = None,
                send_timeout: u8 = 60,
            )
        ),
    )
    .expect("Could not add serve() function to module");
    Ok(())
});
