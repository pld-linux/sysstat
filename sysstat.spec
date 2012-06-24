Summary:	The sar and iostat system monitoring commands
Summary(pl):	Polecenia sar i iostat dla systemu Linux
Summary(ru):	�������� ��������� ���������� ����������� sar � iostat
Summary(uk):	������ ������� ���������� ��Φ������� sar �� iostat
Summary(zh_CN):	sar, iostat ��ϵͳ���ӹ���
Name:		sysstat
Version:	6.0.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.bz2
# Source0-md5:	42670b66b01b830f82e86117659cd43d
Source1:	%{name}.crond
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-opt.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
BuildRequires:	gettext-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the sar and iostat commands for the Linux
operating system, similar to their traditional UNIX counterparts. They
enable system monitoring of disk, network, and other IO activity.

%description -l pl
Pakiet ten udost�pnia polecenia sar i iostat dla systemu Linux podobne
w dzia�aniu do tradycyjnych narz�dzi systemu Unix. Polecenia te
umo�liwiaj� monitorowanie obci��enia zasob�w dyskowych, interfejs�w
sieciowych i innych operacji wej�cia/wyj�cia.

%description -l ru
���� ����� �������� ��������� sar � iostat ��� Linux, ������� ��
������������ ����������� ��������� UNIX. ��� ��������� ������������
���������� ��������, ������� � ������ ���������� �������.

%description -l uk
��� ����� ͦ����� �������� sar �� iostat ��� Linux, ���֦ ��
�����æ�Φ צ���צ�Φ �������� UNIX. ���� ���������� �Ħ��������
��Φ������ ������ϧ, �������ϧ �� ���ϧ ��������Ԧ �������.

%description -l zh_CN
������ṩ������Linux��ϵͳ���ӹ���, ���Լ��Ӵ���, �����Լ� ���� IO
�Ļ���.

%prep
%setup -q
%patch0 -p1

%build
echo "%{_prefix}
%{_prefix}/lib/sa
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
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d,sysconfig},/var/log/sa}

%{__make} install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/sysstat
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sysstat
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sysstat
if [ ! -f /var/lock/subsys/sysstat ]; then
	echo "Run \"/etc/rc.d/init.d/sysstat start\" to start sysstat." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sysstat ]; then
		/etc/rc.d/init.d/sysstat stop >&2
	fi
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
