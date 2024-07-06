use strum::AsRefStr;
use ::ariadne::{Color as AColor, ReportKind as AReportKind};

use pyo3::prelude::*;
use pyo3::types::{PyType, PyTuple};

#[pyclass(module="omniblack.ariadne")]
#[derive(Clone, Debug, AsRefStr)]
pub(crate) enum ReportKind {
    /// The report is an error and indicates a critical problem that prevents
    /// the program performing the requested action.
    Error {},
    /// The report is a warning and indicates a likely problem,
    /// but not to the extent that the requested action cannot be performed.
    Warning {},
    /// The report is advice to the user about a potential anti-pattern
    /// or other benign issues.
    Advice {},

    /// The report is of a kind not built into Ariadne.
    Custom {
        custom: CustomKind,
    },
}

#[pymethods]
impl ReportKind {
    fn __repr__(slf: &Bound<'_, Self>) -> PyResult<String> {
        let py = slf.py();
        let cls: Bound<'_, PyType> = py.get_type_bound::<Self>();
        let cls_name: String = cls.qualname()?;
        let inst = slf.get();
        let inst_name: &str = inst.as_ref();

        return Ok(format!("{cls_name}({inst_name})"));
    }

    fn __rich_repr__<'py>(slf: &'py Bound<'py, Self>) -> PyResult<(&'py str,)> {
        let inst = slf.get();
        let inst_name: &str = inst.as_ref();

        return Ok((inst_name,));
    }
}


#[pyclass(module="omniblack.ariadne")]
#[derive(Clone, Debug)]
pub(crate) struct CustomKind {
    #[pyo3(get, set)]
    name: String,

    #[pyo3(get, set)]
    color: Color,
}

#[pymethods]
impl CustomKind {
    #[new]
    fn py_new(name: String, color: Color) -> Self {
        return CustomKind {
            name,
            color,
        };
    }

    fn __repr__(slf: &Bound<'_, Self>) -> PyResult<String> {
        let py = slf.py();
        let inst = slf.borrow();

        let cls: Bound<'_, PyType> = py.get_type_bound::<Self>();
        let cls_name: String = cls.qualname()?;


        let name = &inst.name;

        let color_py = inst.color.into_py(py);
        let color = color_py.bind(py);
        let color_repr = color.repr()?;

        return Ok(format!("{cls_name}(name={name}, color={color_repr})"));
    }

    fn __rich_repr__<'py>(
        slf: &'py Bound<'py, Self>
    ) -> PyResult<Bound<'py, PyTuple>> {
        let py = slf.py();

        let inst = slf.borrow();
        let name = &inst.name;

        let color_py = inst.color.into_py(py);
        let color = color_py.bind(py);
        let color_repr: String = color.repr()?.extract()?;

        let repr_elements = vec![
            ("name", name),
            ("color", &color_repr),
        ];

        let tuple = PyTuple::new_bound(py, repr_elements);

        return Ok(tuple);
    }
}


impl <'a> From<&'a ReportKind> for AReportKind<'a> {
    fn from(report_kind: &'a ReportKind) -> Self {
        return match report_kind {
            ReportKind::Error {} => AReportKind::Error,
            ReportKind::Warning {} => AReportKind::Warning,
            ReportKind::Advice {} => AReportKind::Advice,
            ReportKind::Custom { custom } => {
                AReportKind::Custom(&custom.name, custom.color.into())
            },
        }
    }
}

impl From<AReportKind<'_>> for ReportKind {
    fn from(report_kind: AReportKind) -> Self {
        return match report_kind {
            AReportKind::Error => ReportKind::Error {},
            AReportKind::Warning => ReportKind::Warning {},
            AReportKind::Advice => ReportKind::Advice {},
            AReportKind::Custom(ref name, color) => {
                ReportKind::Custom {
                    custom: CustomKind {
                        name: name.to_string(),
                        color: color.into(),
                    },
                }
            },
        }
    }
}

#[pyclass(module="omniblack.ariadne")]
#[derive(AsRefStr, Clone, Debug, Copy)]
pub enum Color {
    /// Terminal primary color #9. (foreground code `39`, background code `49`).
    ///
    /// This is the terminal's defined "primary" color, that is, the configured
    /// default foreground and background colors. As such, this color as a
    /// foreground looks "good" against the terminal's default background color,
    /// and this color is a "good" background color for the terminal's default
    /// foreground color.
    Primary {},

    /// A color from 0 to 255, for use in 256-color terminals.
    Fixed { value: u8 },

    /// A 24-bit
    /// <span style="background: red; color: white;">R</span>
    /// <span style="background: green; color: white;">G</span>
    /// <span style="background: blue; color: white;">B</span>
    /// "true color", as specified by ISO-8613-3.
    Rgb { red: u8, green: u8, blue: u8 },

    /// <span style="background: black; color: white;">Black #0</span>
    /// (foreground code `30`, background code `40`).
    Black {},

    /// <span style="background: red; color: white;">Red #1</span>
    /// (foreground code `31`, background code `41`).
    Red {},

    /// <span style="background: green; color: white;">Green: #2</span>
    /// (foreground code `32`, background code `42`).
    Green {},

    /// <span style="background: gold; color: black;">Yellow: #3</span>
    /// (foreground code `33`, background code `43`).
    Yellow {},

    /// <span style="background: blue; color: white;">Blue: #4</span>
    /// (foreground code `34`, background code `44`).
    Blue {},

    /// <span style="background: darkmagenta; color: white;">Magenta: #5</span>
    /// (foreground code `35`, background code `45`).
    Magenta {},

    /// <span style="background: deepskyblue; color: black;">Cyan: #6</span>
    /// (foreground code `36`, background code `46`).
    Cyan {},

    /// <span style="background: #eeeeee; color: black;">White: #7</span>
    /// (foreground code `37`, background code `47`).
    White {},

    /// <span style="background: gray; color: white;">Bright Black #0</span>
    /// (foreground code `90`, background code `100`).
    BrightBlack {},

    /// <span style="background: hotpink; color: white;">Bright Red #1</span>
    /// (foreground code `91`, background code `101`).
    BrightRed {},

    /// <span style="background: greenyellow; color: black;">Bright Green: #2</span>
    /// (foreground code `92`, background code `102`).
    BrightGreen {},

    /// <span style="background: yellow; color: black;">Bright Yellow: #3</span>
    /// (foreground code `93`, background code `103`).
    BrightYellow {},

    /// <span style="background: dodgerblue; color: white;">Bright Blue: #4</span>
    /// (foreground code `94`, background code `104`).
    BrightBlue {},

    /// <span style="background: magenta; color: white;">Bright Magenta: #5</span>
    /// (foreground code `95`, background code `105`).
    BrightMagenta {},

    /// <span style='background: cyan; color: black;'>Bright Cyan: #6</span>
    /// (foreground code `96`, background code `106`).
    BrightCyan {},

    /// <span style="background: white; color: black;">Bright White: #7</span>
    /// (foreground code `97`, background code `107`).
    BrightWhite {},
}

impl From<Color> for AColor {
    fn from(color: Color) -> Self {
         return match color {
            Color::Primary {} => AColor::Primary,
            Color::Fixed { value } => AColor::Fixed(value),
            Color::Rgb { red, green , blue } => {
                AColor::Rgb(red, green, blue)
            },
            Color::Black {} => AColor::Black,
            Color::Red {} => AColor::Red,
            Color::Green {} => AColor::Green,
            Color::Yellow {} => AColor::Yellow,
            Color::Blue {} => AColor::Blue,
            Color::Magenta {} => AColor::Magenta,
            Color::Cyan {} => AColor::Cyan,
            Color::White {} => AColor::White,
            Color::BrightBlack {} => AColor::BrightBlack,
            Color::BrightRed {} => AColor::BrightRed,
            Color::BrightGreen {} => AColor::BrightGreen,
            Color::BrightYellow {} => AColor::BrightYellow,
            Color::BrightBlue {} => AColor::BrightBlue,
            Color::BrightMagenta {} => AColor::BrightMagenta,
            Color::BrightCyan {} => AColor::BrightCyan,
            Color::BrightWhite {} => AColor::BrightWhite,
        }
    }
}

impl From<AColor> for Color {
    fn from(color: AColor) -> Self {
         return match color {
            AColor::Primary => Color::Primary {},
            AColor::Fixed(value) => Color::Fixed{ value },
            AColor::Rgb(red, green , blue) => {
                Color::Rgb { red, green, blue }
            },
            AColor::Black => Color::Black {},
            AColor::Red => Color::Red {},
            AColor::Green => Color::Green {},
            AColor::Yellow => Color::Yellow {},
            AColor::Blue => Color::Blue {},
            AColor::Magenta => Color::Magenta {},
            AColor::Cyan => Color::Cyan {},
            AColor::White => Color::White {},
            AColor::BrightBlack => Color::BrightBlack {},
            AColor::BrightRed => Color::BrightRed {},
            AColor::BrightGreen => Color::BrightGreen {},
            AColor::BrightYellow => Color::BrightYellow {},
            AColor::BrightBlue => Color::BrightBlue {},
            AColor::BrightMagenta => Color::BrightMagenta {},
            AColor::BrightCyan => Color::BrightCyan {},
            AColor::BrightWhite => Color::BrightWhite {},
        }
    }
}

#[pymethods]
impl Color {
    fn __repr__(slf: &Bound<'_, Self>) -> PyResult<String> {
        let py = slf.py();

        let inst = slf.borrow();
        let inst_name = inst.as_ref();

        let cls: Bound<'_, PyType> = py.get_type_bound::<Self>();
        let cls_name: String = cls.qualname()?;


        return match *inst {
            Color::BrightWhite {}
            | Color::BrightCyan {}
            | Color::BrightMagenta {}
            | Color::BrightBlue {}
            | Color::BrightYellow {}
            | Color::BrightGreen {}
            | Color::BrightRed {}
            | Color::BrightBlack {}
            | Color::White {}
            | Color::Cyan {}
            | Color::Magenta {}
            | Color::Blue {}
            | Color::Yellow {}
            | Color::Green {}
            | Color::Red {}
            | Color::Black {}
            | Color::Primary {} =>
                Ok(format!("{cls_name}({inst_name})")),
            Color::Fixed { value } => Ok(
                format!("{cls_name}({inst_name}, {value})")
            ),
            Color::Rgb { red, green, blue } => Ok(
                format!("{cls_name}({inst_name}, red={red}, green={green}, blue={blue})"),
            ),
        };
    }

    fn __rich_repr__<'py>(
        slf: &'py Bound<'py, Self>
    ) -> PyResult<Bound<'py, PyTuple>> {
        let py = slf.py();

        let inst = slf.borrow();
        let inst_name = inst.as_ref();

        return match *inst {
            Color::BrightWhite {}
            | Color::BrightCyan {}
            | Color::BrightMagenta {}
            | Color::BrightBlue {}
            | Color::BrightYellow {}
            | Color::BrightGreen {}
            | Color::BrightRed {}
            | Color::BrightBlack {}
            | Color::White {}
            | Color::Cyan {}
            | Color::Magenta {}
            | Color::Blue {}
            | Color::Yellow {}
            | Color::Green {}
            | Color::Red {}
            | Color::Black {}
            | Color::Primary {} =>
                Ok(PyTuple::new_bound(py, vec![inst_name])),
            Color::Fixed { value } => {
                let items = vec![
                    IntoPy::<Py<PyAny>>::into_py(inst_name, py),
                    IntoPy::<Py<PyAny>>::into_py(value, py),
                ];

                Ok(PyTuple::new_bound(py, items))
            },
            Color::Rgb { red, green, blue } => {
                let items = vec![
                    IntoPy::<Py<PyAny>>::into_py(inst_name, py),
                    IntoPy::<Py<PyAny>>::into_py(("red", red), py),
                    IntoPy::<Py<PyAny>>::into_py(("green", green), py),
                    IntoPy::<Py<PyAny>>::into_py(("blue", blue), py),
                ];

                Ok(PyTuple::new_bound(py, items))
            },
        };
    }
}
