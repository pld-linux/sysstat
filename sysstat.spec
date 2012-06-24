Summary:	The sar and iostat system monitoring commands
Summary(pl):	Polecenia sar i iostat dla systemu Linux
Summary(ru):	�������� ��������� ���������� ����������� sar � iostat
Summary(uk):	������ ������� ���������� ��Φ������� sar �� iostat
Name:		sysstat
Version:	4.0.4
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://perso.wanadoo.fr/sebastien.godard/%{name}-%{version}.tar.bz2
Source1:	%{name}.crond
Source2:	%{name}.init
Patch0:		%{name}-opt.patch
Patch1:		%{name}-verbose.patch
URL:		http://perso.wanadoo.fr/sebastien.godard/
Requires:	crondaemon
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRequires:	gettext-devel
BuildRequires:	sh-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the sar and iostat commands for the Linux
operating system, similar to their traditional UNIX counterparts. They
enable system monitoring of disk, network, and other IO activity.

%description -l pl
Pakiet ten udost�pnia polecenia sar i iostat dla systemu Linux podobne
w dzia�aniu do tradycyjnych narz�dzie systemu Unix. Polecenia te
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

%post
/sbin/chkconfig --add sysstat

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del sysstat
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root)%{_libdir}/sa*
%attr(755,root,root) %dir /var/log/sa
%attr(640,root,root) /etc/cron.d/sysstat
%attr(754,root,root) /etc/rc.d/init.d/sysstat
%{_mandir}/man*/*
