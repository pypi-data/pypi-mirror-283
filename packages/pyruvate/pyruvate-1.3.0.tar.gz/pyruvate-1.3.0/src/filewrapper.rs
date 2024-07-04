#![allow(
    clippy::transmute_ptr_to_ptr,
    clippy::zero_ptr,
    clippy::manual_strip,
    unused_variables
)] // suppress warnings in py_class invocation
use cpython::{
    NoArgs, ObjectProtocol, PyBytes, PyClone, PyObject, PyResult, PyTuple, Python, PythonObject,
    ToPyObject,
};
use errno::errno;
use log::{debug, error};
use std::cell::RefCell;
use std::cmp;
use std::io::Error;
use std::os::unix::io::{AsRawFd, RawFd};

use crate::pyutils::{close_pyobject, with_released_gil};
use crate::transport::would_block;

// This is the maximum the Linux kernel will write in a single sendfile call.
#[cfg(target_os = "linux")]
const SENDFILE_MAXSIZE: isize = 0x7fff_f000;

pub struct SendFileInfo {
    pub content_length: isize,
    pub blocksize: isize,
    pub offset: libc::off_t,
    pub fd: RawFd,
    pub done: bool,
}

impl SendFileInfo {
    pub fn new(fd: RawFd, blocksize: isize) -> Self {
        Self {
            content_length: -1,
            blocksize,
            offset: 0,
            fd,
            done: false,
        }
    }

    // true: chunk written completely, false: there's more
    #[cfg(target_os = "linux")]
    pub fn send_file(&mut self, out: &mut dyn AsRawFd) -> (bool, usize) {
        debug!("Sending file");
        let mut count = if self.blocksize < 0 {
            SENDFILE_MAXSIZE
        } else {
            self.blocksize
        };
        if self.content_length >= 0 {
            count = cmp::min(self.content_length - self.offset as isize, count);
        }
        self.done = (count == 0) || {
            match unsafe {
                libc::sendfile(out.as_raw_fd(), self.fd, &mut self.offset, count as usize)
            } {
                -1 => {
                    // will cover the case where count is too large as EOVERFLOW
                    // s. sendfile(2)
                    let err = Error::from(errno());
                    if !would_block(&err) {
                        error!("Could not sendfile(): {:?}", err);
                        true
                    } else {
                        false
                    }
                }
                // 0 bytes written, assuming we're done
                0 => true,
                _ if (self.content_length > 0) => self.content_length == self.offset as isize,
                // If no content length is given, num_written might be less than count.
                // However the subsequent call will write 0 bytes -> done.
                _ => false,
            }
        };
        (self.done, self.offset as usize)
    }

    #[cfg(target_os = "macos")]
    pub fn send_file(&mut self, out: &mut dyn AsRawFd) -> (bool, usize) {
        debug!("Sending file");
        let mut count: i64 = cmp::max(0, self.blocksize as i64);
        if (self.content_length > 0) && (count > 0) {
            count = cmp::min(self.content_length as i64 - self.offset, count);
        }
        self.done = {
            let res = unsafe {
                libc::sendfile(
                    self.fd,
                    out.as_raw_fd(),
                    self.offset,
                    &mut count,
                    std::ptr::null_mut(),
                    0,
                )
            };
            if count == 0 {
                true
            } else {
                self.offset += count;
                if res == -1 {
                    let err = Error::from(errno());
                    if !would_block(&err) {
                        error!("Could not sendfile(): {:?}", err);
                        true
                    } else {
                        false
                    }
                } else {
                    if self.content_length > 0 {
                        self.content_length <= self.offset as isize
                    } else {
                        false
                    }
                }
            }
        };
        (self.done, self.offset as usize)
    }

    fn update_content_length(&mut self, content_length: isize) {
        self.content_length = content_length;
        if self.blocksize > content_length {
            self.blocksize = content_length;
        }
    }
}

py_class!(pub class FileWrapper |py| {
    data filelike: RefCell<PyObject>;
    data sendfileinfo: RefCell<SendFileInfo>;

    def __new__(_cls, filelike: PyObject, blocksize: Option<isize>=None) -> PyResult<Self> {
        let mut filelike = RefCell::new(filelike);
        let blocksize = blocksize.unwrap_or(-1);
        let mut fd: RawFd = -1;
        if let Ok(fdpyob) = filelike.get_mut().call_method(py, "fileno", NoArgs, None) {
            if let Ok(pyfd) = fdpyob.extract(py) {
                fd = pyfd;
            }
        };
        let sendfileinfo = RefCell::new(SendFileInfo::new(fd, blocksize));
        FileWrapper::create_instance(py, filelike, sendfileinfo)
    }

    def __iter__(&self) -> PyResult<Self> {
        Ok(self.clone_ref(py))
    }

    def __next__(&self) -> PyResult<Option<PyObject>> {
        let py = unsafe { Python::assume_gil_acquired() };
        let sfi = self.sendfileinfo(py).borrow();
        if sfi.fd != -1 {
            return if sfi.done {
                Ok(None)
            } else {
                Ok(Some(PyBytes::new(py, b"").into_object()))
            }
        }
        let bytes = self.filelike(py).borrow_mut().call_method(
            py,
            "read",
            PyTuple::new(
                py,
                &[self
                    .sendfileinfo(py)
                    .borrow()
                    .blocksize
                    .to_py_object(py)
                    .into_object()],
            ),
            None,
        )?;
        if !bytes.is_none(py) && (bytes.get_type(py) == py.get_type::<PyBytes>()) {
            // the following test must avoid memory allocation
            // else iteration will be slow
            if bytes.cast_as::<PyBytes>(py)?.data(py).is_empty() {
                Ok(None)
            } else {
                Ok(Some(bytes))
            }
        } else {
            match close_pyobject(self.as_object(), py) {
                Err(e) => e.print_and_set_sys_last_vars(py),
                Ok(_) => {
                    debug!("WSGIResponse dropped successfully")
                }
            }
            Ok(None)
        }
    }

    def close(&self) -> PyResult<PyObject> {
        match close_pyobject(&self.filelike(py).borrow_mut(), py) {
            Ok(_) => Ok(py.None()),
            Err(e) => Err(e)
        }
    }

});

pub trait SendFile {
    // Put this in a trait for more flexibility.
    fn sendfileinfo<'p>(&'p self, py: Python<'p>) -> &'p RefCell<SendFileInfo>;
    fn send_file(&mut self, out: &mut dyn AsRawFd, py: Python) -> (bool, usize);
    fn update_content_length(&mut self, content_length: usize, py: Python);
    // XXX used only for testing
    #[allow(clippy::new_ret_no_self, dead_code)]
    fn new(py: Python, fd: RawFd, bs: isize) -> PyResult<FileWrapper>;
}

impl SendFile for FileWrapper {
    // public getter
    fn sendfileinfo<'p>(&'p self, py: Python<'p>) -> &'p RefCell<SendFileInfo> {
        self.sendfileinfo(py)
    }

    fn send_file(&mut self, out: &mut dyn AsRawFd, py: Python) -> (bool, usize) {
        with_released_gil(|_threadstate| self.sendfileinfo(py).borrow_mut().send_file(out))
    }

    fn update_content_length(&mut self, content_length: usize, py: Python) {
        self.sendfileinfo(py)
            .borrow_mut()
            .update_content_length(content_length as isize);
    }

    fn new(py: Python, fd: RawFd, bs: isize) -> PyResult<FileWrapper> {
        FileWrapper::create_instance(
            py,
            RefCell::new(py.None()),
            RefCell::new(SendFileInfo::new(fd, bs)),
        )
    }
}

#[cfg(test)]
mod tests {

    use cpython::exc::TypeError;
    use cpython::{
        NoArgs, ObjectProtocol, PyBytes, PyClone, PyDict, PyErr, PyIterator, PyTuple, Python,
        PythonObject, ToPyObject,
    };
    use std::io::{Read, Seek, Write};
    use std::net::{SocketAddr, TcpListener, TcpStream};
    use std::os::unix::io::{AsRawFd, RawFd};
    use std::sync::mpsc::channel;
    use std::thread;
    use tempfile::NamedTempFile;

    use crate::filewrapper::{FileWrapper, SendFile};

    #[test]
    fn test_no_fileno() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fd: RawFd = filelike
                    .call_method(py, "fileno", NoArgs, None)
                    .expect("Could not call fileno method")
                    .extract(py)
                    .expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                if let Ok(fw) = fwany.extract::<FileWrapper>(py) {
                    assert_eq!(fw.sendfileinfo(py).borrow().fd, fd);
                    match PyIterator::from_object(py, fwany) {
                        Ok(mut fwiter) => {
                            for chunk in vec![b"Fo", b"o ", b"42"] {
                                match fwiter.next() {
                                    Some(got) => {
                                        assert_eq!(
                                            chunk,
                                            got.unwrap().extract::<PyBytes>(py).unwrap().data(py)
                                        );
                                    }
                                    None => {
                                        assert!(false);
                                    }
                                }
                            }
                        }
                        Err(_) => assert!(false),
                    }
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_no_read_method() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                match PyIterator::from_object(py, fwany) {
                    Ok(mut fw) => match fw.next() {
                        Some(pyresult) => match pyresult {
                            Ok(_) => assert!(false),
                            Err(_) => assert!(true),
                        },
                        None => {
                            assert!(true);
                        }
                    },
                    Err(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_bytes_not_convertible() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def read(self, blocksize):
        result = 'öäü'
        self.offset += blocksize
        return result

    def fileno(self):
        return -1

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                match PyIterator::from_object(py, fwany) {
                    Ok(mut fw) => match fw.next() {
                        None => {
                            assert!(true);
                        }
                        Some(_) => {
                            assert!(false);
                        }
                    },
                    Err(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_send_file() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let fw = FileWrapper::new(py, f.as_raw_fd(), 4).unwrap();
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"o Wo\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 8);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"rld!\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 12);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"\n\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 13);
        // no content length + blocksize > number bytes written, next should yield some
        sfi.send_file(&mut connection);
        tx.send(()).unwrap();
        t.join().unwrap();
        drop(f);
        // connection is closed now
        let (done, offset) = sfi.send_file(&mut connection);
        assert!(done);
        assert!(offset == 13);
    }

    #[test]
    fn test_send_file_updated_content_length() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let mut fw = FileWrapper::new(py, f.as_raw_fd(), 4).unwrap();
        fw.update_content_length(5, py);
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"o\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 5);
        sfi.send_file(&mut connection);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_send_file_content_length_lt_blocksize() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let mut fw = FileWrapper::new(py, f.as_raw_fd(), 7).unwrap();
        fw.update_content_length(5, py);
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        assert_eq!(sfi.blocksize, 5);
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        sfi.send_file(&mut connection);
        let b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hello\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 5);
        sfi.send_file(&mut connection);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_file_wrapper_new_no_args() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let fwtype = py.get_type::<FileWrapper>();
        match fwtype.call(py, PyTuple::new(py, &[]), None) {
            Err(e) => {
                assert!(py.get_type::<TypeError>() == e.get_type(py));
                // clear error from Python
                PyErr::fetch(py);
            }
            Ok(_) => assert!(false),
        }
    }
}
