Summary:	Per-directory shell configuration tool
Name:		direnv
Version:	2.37.1
Release:	1
License:	MIT
Group:		Applications/Shells
#Source0Download: https://github.com/direnv/direnv/releases
Source0:	https://github.com/direnv/direnv/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e9279513fc4be9a584288366625c0558
# cd %{name}-%{version}
# go mod vendor
# tar cJf ../%{name}-vendor-%{version}.tar.xz vendor
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	4a3cd3046254f03b080ebfe84e3e9389
URL:		https://direnv.net
BuildRequires:	golang >= 1.24
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	xz
ExclusiveArch:	%{go_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	_debugsource_packages

%description
direnv augments existing shells with a new feature that can load and
unload environment variables depending on the current directory.

%prep
%setup -q -a1

%build
%__go build -mod=vendor -o %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md docs version.txt
%attr(755,root,root) %{_bindir}/direnv
%{_mandir}/man1/direnv-fetchurl.1*
%{_mandir}/man1/direnv-stdlib.1*
%{_mandir}/man1/direnv.1*
%{_mandir}/man1/direnv.toml.1*
