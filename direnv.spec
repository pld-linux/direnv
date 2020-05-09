Summary:	Per-directory shell configuration tool
Name:		direnv
Version:	2.21.3
Release:	1
License:	MIT
Group:		Applications/Shells
Source0:	https://github.com/direnv/direnv/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	afab222f7406f90726733f99c095eb0a
URL:		https://direnv.net
BuildRequires:	golang
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# go stuff
%define _enable_debug_packages 0
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v %{?debug:-x} %{?**};
%define import_path	github.com/direnv/direnv

%description
direnv augments existing shells with a new feature that can load and
unload environment variables depending on the current directory.

%prep
%setup -qc
mv %{name}-*/man .
mv %{name}-*/docs .
mv %{name}-*/*.md .
mv %{name}-*/*.txt .

# don't you love go?
install -d src/$(dirname %{import_path})
mv %{name}-* src/%{import_path}
cd src/%{import_path}

%build
export GOPATH=$(pwd)
cd src/%{import_path}
export PATH=$(pwd):$PATH
%gobuild -o $GOPATH/bin/%{name} %{import_path}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs CHANGELOG.md README.md version.txt
%attr(755,root,root) %{_bindir}/direnv
%{_mandir}/man1/direnv-stdlib.1*
%{_mandir}/man1/direnv.1*
%{_mandir}/man1/direnv.toml.1*
