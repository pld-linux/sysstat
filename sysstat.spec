# TODO:
# - solve conflict (obsoletes?):
#   file /usr/bin/iostat from install of sysstat-10.1.6-3.i686 conflicts with file from package iostat-2.2-1.i686
Summary:	The sar and iostat system monitoring commands
Summary(pl.UTF-8):	Polecenia sar i iostat dla systemu Linux
Summary(ru.UTF-8):	Содержит программы системного мониторинга sar и iostat
Summary(uk.UTF-8):	Містить команди системного моніторингу sar та iostat
Summary(zh_CN.UTF-8):	sar, iostat 等系统监视工具
Name:		sysstat
Version:	10.1.6
Release:	4
License:	GPL v2
Group:		Applications/System
Source0:	http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.bz2
# Source0-md5:	61792b2591e4b3adcb7b979af2330fba
Source2:	%{name}.init
Patch0:		%{name}-opt.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	lm_sensors-devel
BuildRequires:	rpmbuild(macros) >= 1.671
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
Requires:	rc-scripts
Requires:	systemd-units >= 38
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
本软件提供了用于Linux的系统监视工具, 可以监视磁盘, 网络以及 其他 IO 的活动情况.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	history=28 \
	compressafter=31 \
	cron_owner=root \
	cron_interval=10 \
	sa_lib_dir=%{_libdir}/sa \
	--enable-install-cron \
	--disable-stripping \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__sed} -i 's/SADC_OPTIONS=""/SADC_OPTIONS="-L"/' sysstat.sysconfig

%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d,sysconfig},/var/log/sa,%{systemdunitdir}}

%{__make} install \
	CHOWN=/bin/true \
	SYSTEMCTL=/bin/true \
	SYSTEMD_UNIT_DIR=$RPM_BUILD_ROOT%{systemdunitdir} \
	DESTDIR=$RPM_BUILD_ROOT

install -p sysstat.service $RPM_BUILD_ROOT%{systemdunitdir}

%{__sed} -e 's|/usr/lib/sa|%{_libdir}/sa|g' %{SOURCE2} >$RPM_BUILD_ROOT/etc/rc.d/init.d/sysstat

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sysstat
%service sysstat restart
%systemd_post sysstat.service

%preun
if [ "$1" = "0" ]; then
	%service sysstat stop
	/sbin/chkconfig --del sysstat
fi
%systemd_preun sysstat.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 10.1.6-1
%systemd_trigger sysstat.service

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README FAQ
%attr(755,root,root) %{_bindir}/cifsiostat
%attr(755,root,root) %{_bindir}/iostat
%attr(755,root,root) %{_bindir}/mpstat
%attr(755,root,root) %{_bindir}/nfsiostat
%attr(755,root,root) %{_bindir}/pidstat
%attr(755,root,root) %{_bindir}/sadf
%attr(755,root,root) %{_bindir}/sar
%dir %{_libdir}/sa
%attr(755,root,root) %{_libdir}/sa/sa*
%attr(750,root,root) %dir /var/log/sa
%attr(754,root,root) /etc/rc.d/init.d/sysstat
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/sysstat
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sysstat
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sysstat.ioconf
%{systemdunitdir}/sysstat.service
%{_mandir}/man1/cifsiostat.1*
%{_mandir}/man1/iostat.1*
%{_mandir}/man1/mpstat.1*
%{_mandir}/man1/nfsiostat.1*
%{_mandir}/man1/pidstat.1*
%{_mandir}/man1/sadf.1*
%{_mandir}/man1/sar.1*
%{_mandir}/man5/sysstat.5*
%{_mandir}/man8/sa1.8*
%{_mandir}/man8/sa2.8*
%{_mandir}/man8/sadc.8*
