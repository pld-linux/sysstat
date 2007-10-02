Summary:	The sar and iostat system monitoring commands
Summary(pl.UTF-8):	Polecenia sar i iostat dla systemu Linux
Summary(ru.UTF-8):	Содержит программы системного мониторинга sar и iostat
Summary(uk.UTF-8):	Містить команди системного моніторингу sar та iostat
Summary(zh_CN.UTF-8):	sar, iostat 等系统监视工具
Name:		sysstat
Version:	8.0.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.bz2
# Source0-md5:	487ee172b2c029ec52ebfd2b803bf8fe
Source1:	%{name}.crond
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-opt.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the sar and iostat commands for the Linux
operating system, similar to their traditional UNIX counterparts. They
enable system monitoring of disk, network, and other IO activity.

%description -l pl.UTF-8
Pakiet ten udostępnia polecenia sar i iostat dla systemu Linux podobne
w działaniu do tradycyjnych narzędzi systemu Unix. Polecenia te
umożliwiają monitorowanie obciążenia zasobów dyskowych, interfejsów
sieciowych i innych operacji wejścia/wyjścia.

%description -l ru.UTF-8
Этот пакет содержит программы sar и iostat для Linux, похожие на
традиционные одноименные программы UNIX. Они позволяют осуществлять
мониторинг дисковой, сетевой и прочей активности системы.

%description -l uk.UTF-8
Цей пакет містить програми sar та iostat для Linux, схожі на
традиційні відповідні програми UNIX. Вони дозволяють здійснювати
моніторинг дискової, мережевої та іншої активності системи.

%description -l zh_CN.UTF-8
本软件提供了用于Linux的系统监视工具, 可以监视磁盘, 网络以及 其他 IO
的活动情况.

%prep
%setup -q
%patch0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d,sysconfig},/var/log/sa}

%{__make} install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/sysstat
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sysstat
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%find_lang %{name}
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sysstat
%service sysstat restart

%preun
if [ "$1" = "0" ]; then
	%service sysstat stop
	/sbin/chkconfig --del sysstat
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README *.sample TODO FAQ
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_prefix}/lib/sa*
%attr(750,root,root) %dir /var/log/sa
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%{_mandir}/man*/*
