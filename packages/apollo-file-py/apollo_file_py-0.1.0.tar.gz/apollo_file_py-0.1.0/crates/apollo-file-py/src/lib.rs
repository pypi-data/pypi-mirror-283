use std::path::PathBuf;
use pyo3::prelude::*;
use apollo_file::ApolloPathBufTrait;

#[pyclass]
pub struct PathBufPy {
    pathbuf: PathBuf
}
#[pymethods]
impl PathBufPy {

    #[new]
    pub fn new() -> Self {
        PathBufPy {
            pathbuf: PathBuf::new(),
        }
    }

    #[staticmethod]
    pub fn new_from_home_dir() -> Self {
        Self {
            pathbuf: PathBuf::new_from_home_dir(),
        }
    }

    #[staticmethod]
    pub fn new_from_documents_dir() -> Self {
        Self {
            pathbuf: PathBuf::new_from_documents_dir(),
        }
    }

    #[staticmethod]
    pub fn new_from_desktop_dir() -> Self {
        Self {
            pathbuf: PathBuf::new_from_desktop_dir(),
        }
    }

    pub fn append(&self, s: &str) -> Self {
        Self {
            pathbuf: self.pathbuf.clone().append(s),
        }
    }

    pub fn to_string(&self) -> String {
        self.pathbuf.to_str().unwrap().to_string()
    }
}

#[pymodule]
fn apollo_file_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PathBufPy>()?;
    Ok(())
}


/*
/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn apollo_file_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
*/
