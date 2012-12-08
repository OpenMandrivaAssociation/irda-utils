Summary:	Utilities for infrared communication between devices
Name:		irda-utils
Version:	0.9.18
Release:	%mkrel 13

Source0:	http://download.sourceforge.net/irda/%{name}-%{version}.tar.gz
Patch0:		irda-utils-0.9.18-chkconfig-pinit-i18n-rh2.patch
Patch2:		irda-utils-0.9.14-typo.patch
Patch4:		irda-utils-0.9.17-rootonly.patch
Patch5:		irda-utils-0.9.15-rh1.patch
Patch7:		irda-utils-0.9.16-tekram-ppc-buildfix.patch
Patch8:		irda-utils-0.9.18-fix-build.patch
Patch12:	irda-utils-0.9.16-io.patch
Patch13:	irda-utils-0.9.18-fix-install.patch
Patch14:	irda-utils-0.9.18-reorder-build.patch
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
%patch14 -p1 -b .reorder

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
%ifnarch ppc %{sunsparc} %mips
%{_sbindir}/findchip
%{_sbindir}/smcinit
%{_sbindir}/tosh1800-smcinit
%{_sbindir}/tosh2450-smcinit
%endif
%{_sbindir}/irdadump
%{_bindir}/irpsion5
%{_bindir}/irkbd
%{_sbindir}/irnetd
%{_initrddir}/irda
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/irda
#%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifcfg-irlan0
%{_mandir}/man?/*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.18-13mdv2011.0
+ Revision: 665523
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.18-12mdv2011.0
+ Revision: 605983
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.18-11mdv2010.1
+ Revision: 520132
- rebuilt for 2010.1

* Fri Sep 25 2009 Olivier Blin <oblin@mandriva.com> 0.9.18-10mdv2010.0
+ Revision: 449113
- enable arch dependant stuff in the spec-file to fix build on mips
  (from Arnaud Patard)

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.9.18-9mdv2010.0
+ Revision: 425386
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.9.18-8mdv2009.1
+ Revision: 351253
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.9.18-7mdv2009.0
+ Revision: 264711
- rebuild early 2009.0 package (before pixel changes)

* Thu May 15 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.9.18-6mdv2009.0
+ Revision: 207508
- make initscript exit with the status of latest operation (fixes #23299)

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 0.9.18-5mdv2008.1
+ Revision: 150344
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Jul 07 2007 Gustavo De Nardin <gustavodn@mandriva.com> 0.9.18-4mdv2008.0
+ Revision: 49587
- P0: unify all patches to the initscript in
  irda-utils-0.9.18-chkconfig-pinit-i18n-rh2.patch, except for the typo one
  which is a coding bugfix by itself
- don't remove unexisting files in prep

* Mon Jul 02 2007 Gustavo De Nardin <gustavodn@mandriva.com> 0.9.18-3mdv2008.0
+ Revision: 46953
- oops, fixed LSB header dependency on $network, it is the other way around...
- declare default runlevels, to prevent chkconfig of not enabling them when
  using just --add
- make irda stop after network

* Mon Jul 02 2007 Gustavo De Nardin <gustavodn@mandriva.com> 0.9.18-1mdv2008.0
+ Revision: 46946
- don't set CFLAGS to make, it breaks the build by overriding its usage in
  the Makefiles
- updated to irda-utils-0.9.18
  - P4: updated to Fedora's irda-utils-0.9.17-rootonly.patch
  - P6: irda-utils-0.9.16-gcc3.4-fix.patch unneeded anymore
  - P8: irda-utils-0.9.17-fix-build.patch updated to also fix build of smcinit
  - P11: irda-utils-0.9.16-glib2.patch unneeded anymore
  - P13: fix Makefile for irnetd install
  - no more auto****, BuildRequires on autoconf2.5 and automake1.4 unneeded
  - BuildRequires: pciutils-devel
  - irdadump is now in /usr/sbin
- bunzipped plain text sources



* Tue Jun 06 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.16-9mdv2007.0
- fix build on sparc
- macroize
- build all with $RPM_OPT_FLAGS
- sync with fedora patches (with rh bugzilla references):
	o load irtty-sir module (P10) (#148750)
	o use glib2 instead of glib (P11) (#136223)
	o don't use asm/io.h directly (P12) (Bastien Nocera #186875)

* Thu Jan 12 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.16-8mdk
- no need to require libtool when only libtoolize is used

* Mon Jan  9 2006 Olivier Blin <oblin@mandriva.com> 0.9.16-7mdk
- convert parallel init to LSB
- Requires(preun)
- mkrel

* Mon Jan  2 2006 Olivier Blin <oblin@mandriva.com> 0.9.16-6mdk
- Patch9: parallel init support
- use Requires(post)

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.9.16-5mdk
- Rebuild

* Mon Jan 31 2005 Frederic Lepied <flepied@mandrakesoft.com> 0.9.16-4mdk
- fix build (gb)

* Thu Jul 15 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.16-3mdk
- fix ppc build

* Thu Jun 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.16-2mdk
- fix gcc-3.4 patch (P6)

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.16-1mdk
- 0.9.16
- sync with fedora patches (P1-P5)
- fix build with gcc-3.4 (P6)
- force use of automake1.4 and autoconf2.5
- fix install
- fix no-prereq-on rpm-helper
- wipe out buildroot at the beginning of %%install, not %%prep
- cosmetics

* Thu Jul 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9.15-1mdk
- 0.9.15

* Mon Sep 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.14-5mdk
- removed ifcfg-irlan0 to avoid lock on some laptops.

* Sat May 26 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.9.14-4mdk
- libtoolize --copy --force before build to make it work with libtool 1.4.
- s/1.2/1.4/ autogen.sh
- s/Copyright/License/;

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.14-3mdk
- use the new rpm macros for servers.

* Mon Jan 29 2001 Stew Benedict <sbenedict@mandrakesoft.com> 0.9.14-2mdk
- disable findchip for PowerPC - not needed - prevents build

* Mon Jan 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.14-1mdk
- new version

* Fri Jan 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.13-2mdk
- corrected typo in init script

* Thu Nov 23 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.13-1mdk
- 0.9.13

* Thu Nov 16 2000 David BAUDENS <baudens@mandrakesoft.com> 0.9.10-2mdk
- Allow to build (fix %%doc)

* Tue Aug 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.10-1mdk
- 0.9.10

* Wed Apr  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.9-1mdk
- group fix.

* Mon Feb  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.9-1mdk
- new version.
- init.d script activated.
- added a printer config file.

* Mon Dec 06 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Wed Nov 10 1999 Dag Brattli <dagb@cs.uit.no>
- 0.9.5
- Some fixes to irattach, so it works with the latest kernels and patches
- Removed OBEX which will now become its own distribution
- Removed irdadump-X11 which will be replaced with a GNOME version

* Wed Sep 8 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 0.9.4
- include new stuff (palm3, psion, obex_tcp, ...)
- various fixes

* Tue Sep 7 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Fix .spec bug

* Tue Sep 7 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- add README to %%doc
- compile gnobex, now in irda-utils-X11

* Tue Sep 7 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- initial RPM:
  - handle RPM_OPT_FLAGS and RPM_BUILD_ROOT
  - fix build
  - split in normal and X11 packages
