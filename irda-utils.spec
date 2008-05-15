Summary:	Utilities for infrared communication between devices
Name:		irda-utils
Version:	0.9.18
Release:	%mkrel 6

Source0:	http://download.sourceforge.net/irda/%{name}-%{version}.tar.gz
Patch0:		irda-utils-0.9.18-chkconfig-pinit-i18n-rh2.patch
Patch2:		irda-utils-0.9.14-typo.patch
Patch4:		irda-utils-0.9.17-rootonly.patch
Patch5:		irda-utils-0.9.15-rh1.patch
Patch7:		irda-utils-0.9.16-tekram-ppc-buildfix.patch
Patch8:		irda-utils-0.9.18-fix-build.patch
Patch12:	irda-utils-0.9.16-io.patch
Patch13:	irda-utils-0.9.18-fix-install.patch
Group:		System/Servers
URL:		http://irda.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
BuildRequires:	glib2-devel
BuildRequires:	pciutils-devel
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description
IrDA(TM) (Infrared Data Association) is an industry standard for
wireless, infrared communication between devices. IrDA speeds range
from 9600 bps to 4 Mbps, and IrDA can be used by many modern devices
including laptops, LAN adapters, PDAs, printers, and mobile phones.

The Linux-IrDA project is a GPL'd implementation, written from
scratch, of the IrDA protocols. Supported IrDA protocols include
IrLAP, IrLMP, IrIAP, IrTTP, IrLPT, IrLAN, IrCOMM and IrOBEX.

The irda-utils package contains a collection of programs that enable
the use of IrDA protocols. Most IrDA features are implemented in the
kernel, so IrDA support must be enabled in the kernel before any IrDA
tools or programs can be used. Some configuration outside the kernel
is required, however, and some IrDA features, like IrOBEX, are
actually implemented outside the kernel.

%prep
%setup -q
%patch0 -p1 -b .irda.rc-fixes
%patch2 -p1 -b .typo
%patch4 -p1 -b .rootonly
%patch5 -p1 -b .rh1
%patch7 -p1 -b .tekram-ppc-buildfix
%patch8 -p1 -b .fix-build
%patch12 -p1 -b .io
%patch13 -p1 -b .fix-install

%build
%serverbuild
%make all

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_initrddir}}

%makeinstall_std  ROOT="$RPM_BUILD_ROOT" MANDIR="$RPM_BUILD_ROOT%{_mandir}"

for dir in irattach irdadump irdaping tekram; do
    cp $dir/README $dir/README.$dir
done
mv smcinit/README.Peri smcinit/README.tosh1800-smcinit
mv smcinit/README smcinit/README.smcinit
mv smcinit/README.Tom smcinit/README.Tom.scminit
mv smcinit/README.Rob smcinit/README.Rob.smcinit
mv smcinit/RobMiller-irda.html smcinit/README.Rob.smcinit.html

rm -f $RPM_BUILD_ROOT/etc/sysconfig/network-scripts/ifcfg-irlan0

%post
%_post_service irda

%preun
%_preun_service irda

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README
%doc irattach/README.irattach
%doc irdadump/README.irdadump
%doc irdaping/README.irdaping
%doc tekram/README.tekram
%doc smcinit/README*
%{_sbindir}/irattach
%{_sbindir}/irdaping
%{_sbindir}/dongle_attach
%ifnarch ppc %{sunsparc}
%{_sbindir}/findchip
%endif
%{_sbindir}/irdadump
%{_bindir}/irpsion5
%{_bindir}/irkbd
%{_sbindir}/irnetd
%{_sbindir}/smcinit
%{_sbindir}/tosh1800-smcinit
%{_sbindir}/tosh2450-smcinit
%{_initrddir}/irda
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/irda
#%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifcfg-irlan0
%{_mandir}/man?/*
