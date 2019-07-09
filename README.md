# MIT OCW 6.0001 Problem Sets

Solutions for [problem
sets](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/assignments/)
from the [MIT OCW 6.0001
course](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/index.htm).

## Installation

> Prerequisites: Python 3.5 or greater

Clone the repository:
```sh
$ git clone https://github.com/synicalsyntax/6.0001.git path/to/6.0001
```

Install dependencies with [pip](https://pip.pypa.io/en/stable/) after
navigating to the repository directory:
```sh
$ cd path/to/6.0001
$ pip install -r requirements.txt
```

## Style

* The code attempts to follow the [6.0001 Style
  Guide](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/assignments/MIT6_0001F16_StyleGuide.pdf)
  as closely as possible.
* Problem set code (excludes test suites and utility modules) follows the [PEP
  8 specification](https://www.python.org/dev/peps/pep-0008/) (linted with
  [Flake8](http://flake8.pycqa.org/en/latest/manpage.html)). As a result, some
  helper methods and docstrings have been modified to fit PEP 8 standards (e.g.
  maximum line length).
    * [List comprehensions are used over lambda
      functions.](https://www.artima.com/weblogs/viewpost.jsp?thread=98196)
* Docstrings for self-implemented methods and classes follow the [PEP 287
  specification](https://www.python.org/dev/peps/pep-0287/) (reST format). The
  content for docstrings initially implemented by the instructor(s) has not
  been modified.

## Contributing
Please create an issue in the [GitHub issue
tracker](https://github.com/synicalsyntax/6.0001/issues) for any bug reports,
suggestions, or other comments.

## License

[MIT License](LICENSE)
