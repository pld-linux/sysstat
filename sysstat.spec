Summary:	SAR, MPSTAT and IOSTAT for Linux
Summary(pl):	SAR, MPSTAT and IOSTAT dla Linuxa
Name:		sysstat
Version:	4.0.0
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.bz2
Source1:	%{name}.crond
Source2:	%{name}.init
Patch0:		%{name}-opt.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
Requires:       crondaemon
Requires:	rc-scripts
BuildRequires:	gettext-devel
BuildRequires:	sh-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SAR, MPSTAT and IOSTAT for Linux.

%description -l pl
SAR, MPSTAT and IOSTAT dla Linuxa.

%prep
%setup -q
%patch0 -p1

%build
echo "%{_prefix}
/var/log/sa
n
y
n
`id -gn`
n" | /bin/sh build/Configure.sh

OPT_FLAGS="%{rpmcflags}" %{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d},/var/log/sa}

%{__make} install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/sysstat
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sysstat

gzip -9nf CHANGES CREDITS README *.sample TODO

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root)%{_libdir}/sa*
%attr(755,root,root) %dir /var/log/sa
%attr(640,root,root) /etc/cron.d/sysstat
%attr(754,root,root) /etc/rc.d/init.d/sysstat
%{_mandir}/man*/*

%post
/sbin/chkconfig --add sysstat
