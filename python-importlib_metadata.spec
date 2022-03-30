#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (for Python < 3.8; newer built from python3-importlib_metadata.spec)

Summary:	Read metadata from Python packages
Summary(pl.UTF-8):	Odczyt metadanych z pakietów Pythona
Name:		python-importlib_metadata
# keep 2.x here for python2 support
Version:	2.1.3
Release:	5
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/importlib-metadata/
Source0:	https://files.pythonhosted.org/packages/source/i/importlib-metadata/importlib_metadata-%{version}.tar.gz
# Source0-md5:	10bf15d611e8d61d6f7b3aa112196fca
URL:		https://pypi.org/project/importlib-metadata/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:30.3
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-configparser >= 3.5
BuildRequires:	python-contextlib2
BuildRequires:	python-importlib_resources >= 1.3
BuildRequires:	python-packaging
BuildRequires:	python-pathlib2
BuildRequires:	python-pep517
BuildRequires:	python-pyfakefs
BuildRequires:	python-unittest2
BuildRequires:	python-zipp >= 0.5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:30.3
BuildRequires:	python3-setuptools_scm
%if %{with tests}
%if "%{_ver_lt '%{py3_ver}' '3.9'}" == "1"
BuildRequires:	python3-importlib_resources >= 1.3
%endif
BuildRequires:	python3-packaging
BuildRequires:	python3-pep517
BuildRequires:	python3-pyfakefs
BuildRequires:	python3-zipp >= 0.5
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.749
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python-rst.linker
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
importlib_metadata is a library to access the metadata for a Python
package. It is intended to be ported to Python 3.8.

%description -l pl.UTF-8
importlib_metadata to biblioteka służąca do dostępu do metadanych
pakietów Pythona. Ma być przeniesiona do Pythona 3.8.

%package -n python3-importlib_metadata
Summary:	Read metadata from Python packages
Summary(pl.UTF-8):	Odczyt metadanych z pakietów Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-importlib_metadata
importlib_metadata is a library to access the metadata for a Python
package. It is intended to be ported to Python 3.8.

%description -n python3-importlib_metadata -l pl.UTF-8
importlib_metadata to biblioteka służąca do dostępu do metadanych
pakietów Pythona. Ma być przeniesiona do Pythona 3.8.

%package apidocs
Summary:	API documentation for Python importlib_metadata module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona importlib_metadata
Group:		Documentation

%description apidocs
API documentation for Python importlib_metadata module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona importlib_metadata.

%prep
%setup -q -n importlib_metadata-%{version}

%{__sed} -i -e '/LocalProjectTests/ i@unittest.skip("requires network")' tests/test_integration.py

%build
export LC_ALL=C.UTF-8
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest2 discover -s tests -t $(pwd)
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s tests -t $(pwd)
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/importlib_metadata
%{py_sitescriptdir}/importlib_metadata-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-importlib_metadata
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/importlib_metadata
%{py3_sitescriptdir}/importlib_metadata-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
