use std::io::Cursor;
use std::ops::Range;
use std::fmt::{Debug, Display};
use std::path::Path;

use ::ariadne::{
    Label as _ALabel,
    Report as _AReport,
    ReportBuilder as _ReportBuilder,
    Config,
    IndexType,
};
use pyo3::prelude::*;
use pyo3::types::{PyString, PyLong, PyType, PyTuple};
use ::ariadne::{
    Cache, FileCache as _FileCache, Source
};

mod wrappers;
use wrappers::{Color, ReportKind};

type SpanType = (String, Range<usize>);
type ALabel = _ALabel<SpanType>;
type AReport<'a> = _AReport<'a, SpanType>;
type ReportBuilder<'a> = _ReportBuilder<'a, SpanType>;


#[derive(Default)]
struct FileCache(_FileCache);

impl Cache<String> for FileCache {
    type Storage = String;

    fn fetch(&mut self, path: &String) -> Result<&Source, Box<dyn Debug + '_>> {
        return self.0.fetch(Path::new(path));
    }

    fn display<'a>(&self, path: &'a String) -> Option<Box<dyn Display + 'a>> {
        Some(Box::new(path))
    }
}

#[pyclass(module="omniblack.ariadne", get_all, set_all)]
#[derive(Debug, Clone)]
struct Label {
    msg: Py<PyString>,
    filename: Py<PyString>,
    start: Py<PyLong>,
    end: Py<PyLong>,
    color: Option<Py<Color>>,
    order: Py<PyLong>,
    priority: Py<PyLong>,
}

fn  to_repr<'py, T: ToPyObject> (
    py: Python<'py>,
    slf: &Py<T>,
) -> PyResult<Bound<'py, PyString>> {
    let bound = slf.to_object(py);
    let any: &Bound<'py, PyAny> = bound.bind(py);
    return any.repr();
}


fn zero_default(py: Python<'_>) -> PyResult<Py<PyLong>> {
    let value: PyObject = IntoPy::<PyObject>::into_py(0i64, py);
    let bound = value.bind(py);
    let long = bound.downcast::<PyLong>()?;
    return Ok(long.clone().unbind());

}

#[pymethods]
impl Label {
    #[new]
    #[pyo3(signature=(
        msg,
        *,
        filename,
        start,
        end,
        color=None,
        order=None,
        priority=None,
    ))]
    fn py_new(
        py: Python<'_>,
        msg: Py<PyString>,
        filename: Py<PyString>,
        start: Py<PyLong>,
        end: Py<PyLong>,
        color: Option<Py<Color>>,
        order: Option<Py<PyLong>>,
        priority: Option<Py<PyLong>>,
    ) -> PyResult<Self> {

        let order = match order {
            Some(v) => v,
            None => zero_default(py)?,
        };

        let priority = match priority {
            Some(v) => v,
            None => zero_default(py)?,
        };

        return Ok(Label {
            msg,
            filename,
            start,
            end,
            color,
            order,
            priority,
        });
    }

    fn __repr__<'py>(slf: &'py Bound<'py, Self>) -> PyResult<String> {
        let py = slf.py();
        let cls: Bound<'_, PyType> = py.get_type_bound::<Self>();
        let cls_name: String = cls.qualname()?;

        let inst = slf.borrow();

        let color = inst.color.clone().into_py(py);

        let msg = to_repr(py, &inst.msg)?;
        let file = to_repr(py, &inst.filename)?;
        let color = to_repr(py, &color)?;
        let order = to_repr(py, &inst.order)?;
        let priority = to_repr(py, &inst.priority)?;
        let start = to_repr(py, &inst.start)?;
        let end = to_repr(py, &inst.end)?;

        return Ok(format!(
            "{cls_name}({file}, msg={msg}, color={color}, order={order}, priority={priority}, start={start}, end={end})"
        ));
    }

    fn __rich_repr__<'py>(slf: &'py Bound<'py, Self>) -> Bound<'py, PyTuple> {
        let py = slf.py();
        let inst = slf.borrow();

        let color = inst.color.clone().into_py(py);

        let items = vec![
            inst.msg.to_object(py),
            IntoPy::into_py(("filename", &inst.filename), py),
            IntoPy::into_py(("color", color), py),
            IntoPy::into_py(("order", &inst.order, 0), py),
            IntoPy::into_py(("priority", &inst.priority, 0), py),
            IntoPy::into_py(("start", &inst.start), py),
            IntoPy::into_py(("end", &inst.end), py),
        ];

        return PyTuple::new_bound(py, items);
    }

}

impl Label {
    fn to_rust(
        &self,
        py: Python<'_>,
    ) -> PyResult<ALabel> {
        let filename: String = self.filename.extract(py)?;
        let start: usize = self.start.extract(py)?;
        let end: usize = self.end.extract(py)?;

        let mut label = ALabel::new((filename, start..end));

        let message: &str = self.msg.extract(py)?;

        label = label.with_message(message);

        if let Some(color) = &self.color {
            let color: Color = *color.borrow(py);
            label = label.with_color(color.into());
        }

        label = label.with_order(self.order.extract(py)?);
        label = label.with_priority(self.priority.extract(py)?);

        return Ok(label);
    }
}

#[pyclass(module="omniblack.ariadne", get_all, set_all)]
#[derive(Debug, Clone)]
struct Report {
    kind: ReportKind,
    filename: Py<PyString>,
    msg: Py<PyString>,
    offset: Py<PyLong>,
    code: Option<Py<PyString>>,
    note: Option<Py<PyString>>,
    help: Option<Py<PyString>>,
    labels: Vec<Label>,
}

#[pymethods]
impl Report {
    #[new]
    #[pyo3(
        signature=(
            msg,
            *,
            kind,
            filename,
            offset,
            code=None,
            note=None,
            help=None,
            labels=vec![],
        )
    )]
    fn py_new(
        msg: Py<PyString>,
        kind: ReportKind,
        filename: Py<PyString>,
        offset: Py<PyLong>,
        code: Option<Py<PyString>>,
        note: Option<Py<PyString>>,
        help: Option<Py<PyString>>,
        labels: Vec<Label>,
    ) -> Self {
        return Report {
            kind,
            filename,
            offset,
            code,
            msg,
            note,
            help,
            labels,
        };
    }


    fn __str__<'py>(slf: &'py Bound<'py, Self>) -> PyResult<String> {
        let py = slf.py();
        let inst = slf.borrow();

        let mut buffer = Cursor::new(vec![0; 100]);
        let cache = FileCache::default();

        let final_report = inst.to_rust(py)?;
        final_report.write(cache, &mut buffer)?;
        let report_str = String::from_utf8(buffer.into_inner())?;

        return Ok(report_str);
    }
}

impl Report {
    fn to_rust(&self, py: Python<'_>) -> PyResult<AReport> {
        let kind: ::ariadne::ReportKind = (&self.kind).into();
        let filename: String = self.filename.extract(py)?;
        let mut report: ReportBuilder = AReport::build(
            kind,
            filename,
            self.offset.extract(py)?,
        );

        let msg: String = self.msg.extract(py)?;
        report = report.with_message(msg);

        if let Some(code) = &self.code {
            let code: String = code.extract(py)?;
            report = report.with_code(code);
        }

        if let Some(note) = &self.note {
            let note: String = note.extract(py)?;
            report = report.with_note(note);
        }

        if let Some(help) = &self.help {
            let help: String = help.extract(py)?;
            report = report.with_help(help);
        }

        let labels: PyResult<Vec<ALabel>> = self.labels
            .iter()
            .map(|label| -> PyResult<ALabel> { label.to_rust(py) })
            .collect();
        let labels = labels?;
        report.add_labels(labels);

        let config = Config::default()
            .with_index_type(IndexType::Char);

        report = report.with_config(config);

        return Ok(report.finish());
    }
}

#[pymodule]
fn ariadne(_py: Python, m: Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Color>()?;
    m.add_class::<ReportKind>()?;
    m.add_class::<Label>()?;
    m.add_class::<Report>()?;
    return Ok(());
}
