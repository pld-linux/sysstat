Summary:	SAR, MPSTAT and IOSTAT for Linux
Summary(pl):	SAR, MPSTAT and IOSTAT dla Linuxa
Name:		sysstat
Version:	3.3.4
Release:	1
License:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	http://www.ibiblio.org/pub/Linux/system/status/%{name}-%{version}.tar.gz
Patch0:		sysstat-opt.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
BuildRequires:	gettext-devel
BuildRequires:	sh-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SAR, MPSTAT and IOSTAT for Linux

%description -l pl
SAR, MPSTAT and IOSTAT dla Linuxa

%prep
%setup -q
%patch0 -p1

%build
echo "%{_prefix}
y
n
`id -gn`
n" | /bin/sh build/Configure.sh

OPT_FLAGS="%{?debug:-O0 -g}%{!?debug:$RPM_OPT_FLAGS}" %{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install

gzip -9nf CHANGES CREDITS README *.sample TODO

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_libdir}/sa
%{_mandir}/man*/*
