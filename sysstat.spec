%bcond_without	systemd	# systemd
#
# Fix or remove  install.patch (seems systemd files are installed now)
Summary:	The sar and iostat system monitoring commands
Summary(pl.UTF-8):	Polecenia sar i iostat dla systemu Linux
Summary(ru.UTF-8):	Содержит программы системного мониторинга sar и iostat
Summary(uk.UTF-8):	Містить команди системного моніторингу sar та iostat
Summary(zh_CN.UTF-8):	sar, iostat 等系统监视工具
# use stable versions
# Sysstat 12.?.x released (development version).
# Sysstat 12.6.x released (stable version).
Name:		sysstat
Version:	12.6.1
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://pagesperso-orange.fr/sebastien.godard/%{name}-%{version}.tar.xz
# Source0-md5:	c8d6a6799c0851497fed0fec89f26eb8
Source2:	%{name}.init
Source3:	crontab
Patch1:		install.patch
URL:		http://sebastien.godard.pagesperso-orange.fr/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	lm_sensors-devel
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires:	cronjobs
Requires:	rc-scripts
Requires:	systemd-units >= 38
Requires:	xz
Obsoletes:	iostat
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/lib/sa

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
%patch -P1 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	history=28 \
	compressafter=31 \
	cron_owner=root \
	cron_interval=1 \
	sadc_options='-L -S XDISK' \
	sa_lib_dir=%{_libexecdir} \
	ZIP=%{_bindir}/xz \
	--enable-install-cron \
	--disable-compress-manpg \
	--disable-stripping \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__sed} -i 's/SADC_OPTIONS=""/SADC_OPTIONS="-L -S XDISK"/' sysstat.sysconfig

%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d,sysconfig},/var/log/sa,%{systemdunitdir}}

%{__make} install \
	CHOWN=/bin/true \
	SYSTEMCTL=/bin/true \
	SYSTEMD_UNIT_DIR=%{systemdunitdir} \
	DESTDIR=$RPM_BUILD_ROOT \
	IGNORE_MAN_GROUP=y \
	IGNORE_FILE_ATTRIBUTES=y

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sysstat
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/%{name}

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

%triggerpostun -- %{name} < %{version}-%{release}
# < 10.1.6-1
%systemd_trigger sysstat.service
# < 12.2.0-2
C=0
for log in /var/log/sa/sa[0-9]*; do
	if (LC_ALL=C %{_bindir}/sadf -C "$log" 2>&1 | grep -q "Current sysstat version cannot read the format of this file"); then
		echo "Converting file $log to current format: "
		if (%{_bindir}/sadf -c "$log" > "$log.migrate"); then
			chown --reference "$log" "$log.migrate"
			chmod --reference "$log" "$log.migrate"
			mv "$log.migrate" "$log"
			C=1
		else
			echo "$log MIGRATION FAILED." >&2
		fi
	fi
done
if [ "$C" -eq 1 ]; then
	%service sysstat restart
	%systemd_post sysstat.service
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README.md FAQ.md
%attr(755,root,root) %{_bindir}/cifsiostat
%attr(755,root,root) %{_bindir}/iostat
%attr(755,root,root) %{_bindir}/mpstat
%attr(755,root,root) %{_bindir}/tapestat
%attr(755,root,root) %{_bindir}/pidstat
%attr(755,root,root) %{_bindir}/sadf
%attr(755,root,root) %{_bindir}/sar
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/sa1
%attr(755,root,root) %{_libexecdir}/sa2
%attr(755,root,root) %{_libexecdir}/sadc
%attr(754,root,root) /etc/rc.d/init.d/sysstat
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/sysstat
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sysstat
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sysstat.ioconf
%if %{with systemd}
%{systemdunitdir}/sysstat.service
%{systemdunitdir}/sysstat-collect.service
%{systemdunitdir}/sysstat-collect.timer
%{systemdunitdir}/sysstat-summary.service
%{systemdunitdir}/sysstat-summary.timer
%{systemdunitdir}-sleep/sysstat.sleep
%endif
%{_mandir}/man1/cifsiostat.1*
%{_mandir}/man1/iostat.1*
%{_mandir}/man1/mpstat.1*
%{_mandir}/man1/tapestat.1*
%{_mandir}/man1/pidstat.1*
%{_mandir}/man1/sadf.1*
%{_mandir}/man1/sar.1*
%{_mandir}/man5/sysstat.5*
%{_mandir}/man8/sa1.8*
%{_mandir}/man8/sa2.8*
%{_mandir}/man8/sadc.8*
%attr(750,root,root) %dir /var/log/sa
