Summary:	The sar and iostat system monitoring commands
Summary(pl):	Polecenia sar i iostat dla systemu Linux
Summary(ru):	Содержит программы системного мониторинга sar и iostat
Summary(uk):	М╕стить команди системного мон╕торингу sar та iostat
Summary(zh_CN):	sar, iostat ╣хо╣мЁ╪Юйс╧╓╬ъ
Name:		sysstat
Version:	4.1.3
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.bz2
# Source0-md5:	ce24f45bc5bc8af94ed3c28636ebf4a3
Source1:	%{name}.crond
Source2:	%{name}.init
Patch0:		%{name}-opt.patch
Patch1:		%{name}-verbose.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
BuildRequires:	gettext-devel
BuildRequires:	sh-utils
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the sar and iostat commands for the Linux
operating system, similar to their traditional UNIX counterparts. They
enable system monitoring of disk, network, and other IO activity.

%description -l pl
Pakiet ten udostЙpnia polecenia sar i iostat dla systemu Linux podobne
w dziaЁaniu do tradycyjnych narzЙdzi systemu Unix. Polecenia te
umo©liwiaj╠ monitorowanie obci╠©enia zasobСw dyskowych, interfejsСw
sieciowych i innych operacji wej╤cia/wyj╤cia.

%description -l ru
Этот пакет содержит программы sar и iostat для Linux, похожие на
традиционные одноименные программы UNIX. Они позволяют осуществлять
мониторинг дисковой, сетевой и прочей активности системы.

%description -l uk
Цей пакет м╕стить програми sar та iostat для Linux, схож╕ на
традиц╕йн╕ в╕дпов╕дн╕ програми UNIX. Вони дозволяють зд╕йснювати
мон╕торинг дисково╖, мережево╖ та ╕ншо╖ активност╕ системи.

%description -l zh_CN
╠╬хМ╪ЧлА╧╘аксцсзLinux╣до╣мЁ╪Юйс╧╓╬ъ, ©ирт╪Юйс╢еел, мЬбГрт╪╟
фДкШ IO ╣д╩Н╤╞гИ©Ж.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
echo "%{_prefix}
/var/log/sa
n
y
n
y
7
`id -gn`
n" | /bin/sh build/Configure.sh

%{__make} \
	CC="%{__cc}" \
	OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d},/var/log/sa}

%{__make} install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/sysstat
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sysstat

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sysstat

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del sysstat
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README *.sample TODO FAQ
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %{_libdir}/sa*
%attr(755,root,root) %dir /var/log/sa
%attr(640,root,root) /etc/cron.d/sysstat
%attr(754,root,root) /etc/rc.d/init.d/sysstat
%{_mandir}/man*/*
