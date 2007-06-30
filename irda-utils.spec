Summary:	Utilities for infrared communication between devices
Name:		irda-utils
Version:	0.9.16
Release:	%mkrel 9

Source0:	http://download.sourceforge.net/irda/%{name}-%{version}.tar.bz2
Patch1:		irda-utils-0.9.14-chkconfig.patch
Patch2:		irda-utils-0.9.14-typo.patch
Patch3:		irda-utils-0.9.13-i18n.patch
Patch4:		irda-utils-0.9.16-rootonly.patch
Patch5:		irda-utils-0.9.15-rh1.patch
Patch6:		irda-utils-0.9.16-gcc3.4-fix.patch
Patch7:		irda-utils-0.9.16-tekram-ppc-buildfix.patch
Patch8:		irda-utils-0.9.17-fix-build.patch
Patch9:		irda-utils-0.9.16-pinit.patch
Patch10:	irda-utils-0.9.16-rh2.patch
Patch11:	irda-utils-0.9.16-glib2.patch
Patch12:	irda-utils-0.9.16-io.patch
Group:		System/Servers
URL:		http://irda.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
BuildRequires:	glib2-devel autoconf2.5 automake1.4
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
%patch1 -p1 -b .chkconfig
%patch2 -p1 -b .typo
%patch3 -p1 -b .i18n
%patch4 -p1 -b .root
%patch5 -p1 -b .rh1
%patch6 -p1 -b .gcc3.4
%patch7 -p1 -b .tekram-ppc-buildfix
%patch8 -p1 -b .fix-build
%patch9 -p1 -b .pinit
%patch10 -p1 -b .rh2
%patch11 -p1 -b .glib2
%patch12 -p1 -b .io
rm -f irdadump/{install-sh,mkinstalldirs,missing}

%build
export FORCE_AUTOCONF_2_5=1
%serverbuild
# autogen.sh sucks.
cd irdadump && libtoolize --copy --force && \
perl -pi -e s/1\.2/1\.4/ autogen.sh && \
perl -pi -e "s#libtool #libtoolize #g" autogen.sh && \
perl -pi -e "s#automake#automake-1.4#g" autogen.sh && \
perl -pi -e "s#aclocal#aclocal-1.4#g" autogen.sh && cd ..
%make all RPM_BUILD_ROOT="$RPM_BUILD_ROOT" RPM_OPT_FLAGS="$RPM_OPT_FLAGS" ROOT="$RPM_BUILD_ROOT" CFLAGS="$RPM_OPT_FLAGS -I../include"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_initrddir}}

%makeinstall  ROOT="$RPM_BUILD_ROOT" MANDIR="$RPM_BUILD_ROOT%{_mandir}"

for dir in irattach irdadump irdaping tekram; do
    cp $dir/README $dir/README.$dir
done

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
%{_sbindir}/irattach
%{_sbindir}/irdaping
%{_sbindir}/dongle_attach
%ifnarch ppc %{sunsparc}
%{_sbindir}/findchip
%endif
%{_bindir}/irdadump
%{_bindir}/irpsion5
%{_bindir}/irkbd
%{_initrddir}/irda
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/irda
#%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifcfg-irlan0
%{_mandir}/man?/*
