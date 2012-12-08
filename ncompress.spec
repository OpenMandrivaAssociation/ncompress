%define	name	ncompress
%define	oname	compress
%define	version	4.2.4.4
%define	release	%mkrel 3

Summary:	Fast compression and decompression utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Archiving/Compression
URL:		http://ncompress.sourceforge.net/
Source:		http://downloads.sourceforge.net/ncompress/%{name}-%{version}.tar.gz
Patch0:		ncompress-4.2.4-make.patch
Patch1:		ncompress-4.2.4-lfs2.patch
Patch2:		ncompress-4.2.4.2-filenamelen.patch
Patch3:		ncompress-2GB.patch
Patch6: 	ncompress-4.2.4-endians.patch
Patch7:		ncompress-4.2.4.2-LDFLAGS.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The ncompress package contains the compress and uncompress
file compression and decompression utilities, which are compatible
with the original UNIX compress utility (.Z file extensions).  These
utilities can't handle gzipped (.gz file extensions) files, but
gzip can handle compressed files.

%prep

%setup -q
%patch0 -p1
%patch1 -p0 -b .lfs
%patch2 -p1 -b .filenamelen
%patch3 -p1 -b .2gb
%patch6 -p1 -b .endians
%patch7 -p0 -b .LDFLAGS

%build
#- extra CFLAGS
%ifarch alpha ia64
EXTRA_FLAGS="-DNOALIGN=0"
%endif
ENDIAN_FLAGS=4321

%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ENDIAN_FLAGS=1234
%endif

%make RPM_OPT_FLAGS="%{optflags} $ARCH32_FLAGS $EXTRA_FLAGS" ENDIAN="$ENDIAN_FLAGS" LDFLAGS="%{ldflags}"

%install
rm -rf %{buildroot}
install -m755 %{oname} -D %{buildroot}%{_bindir}/%{oname}
ln -sf %{oname} %{buildroot}%{_bindir}/uncompress
install -m644 %{oname}.1 -D %{buildroot}%{_mandir}/man1/%{oname}.1
ln -sf %{oname}.1.bz2 %{buildroot}%{_mandir}/man1/uncompress.1.bz2

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%doc LZW.INFO README Changes Acknowleds


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 4.2.4.4-2mdv2011.0
+ Revision: 666600
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 4.2.4.4-1mdv2011.0
+ Revision: 607031
- 4.2.4.4
- rebuild

* Mon Mar 08 2010 Sandro Cazzaniga <kharec@mandriva.org> 4.2.4.3-1mdv2010.1
+ Revision: 516719
- update to 4.2.4.3

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 4.2.4.2-4mdv2010.0
+ Revision: 426229
- rebuild

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 4.2.4.2-3mdv2009.1
+ Revision: 319055
- rediffed one fuzzy patch
- use %%ldflags

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 4.2.4.2-2mdv2009.0
+ Revision: 223336
- rebuild

* Sun Mar 02 2008 Olivier Blin <oblin@mandriva.com> 4.2.4.2-1mdv2008.1
+ Revision: 177755
- remove most of the filenamelen patch, "filename too long" errors are already handled upstream
- remove bssUnderflow patch (merged upstream)
- remove zero byte patch (merged upstream)
- rediff filenamelen patch (remove rindex hunks, replaced by strrchr now)
- bunzip2 patches
- update URL to SourceForge project
- 4.2.4.2

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 4.2.4-36mdv2008.1
+ Revision: 153280
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Sep 11 2007 Olivier Thauvin <nanardon@mandriva.org> 4.2.4-34mdv2008.0
+ Revision: 84366
- really fix on 64bits arch

* Wed Aug 29 2007 Olivier Thauvin <nanardon@mandriva.org> 4.2.4-33mdv2008.0
+ Revision: 75018
- from Philippe Weill <Philippe.Weill@aero.jussieu.fr>
  o P6 and P7 from fedora core 7 for endian and fix uncompress on x86_64
  o removed old endian stuff

* Wed Aug 29 2007 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-32mdv2008.0
+ Revision: 73426
- Import ncompress



* Tue Sep 05 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.2.4-32mdv2007.0
- cosmetics
- P5 from fedora:
	o fix problems with compressing zero-sized files (rh #189215, rh #189216)

* Tue Aug 29 2006 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-31
- added fixes from 4.2.4-28.1.20060mdk:
  - P4: security fix for CVE-2006-1168

* Fri Jan 27 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 4.2.4-30mdk
- generic build, thus also enabling ppc64

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 4.2.4-29mdk
- Rebuild

* Wed Dec 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 4.2.4-28mdk
- permit files > 2GB to be compressed (P3 from fedora)
- add sparcv9 sparc64 & ppc64 to arch flags

* Thu Oct 21 2004 Giuseppe Ghibó <ghibo@mandrakesoft.com> 4.2.4-27mdk
- added x86_64 to arch flags.

* Sun Aug 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 4.2.4-26mdk
- rebuild

* Mon Apr 19 2004 Michael Scherer <misc@mandrake.org> 4.2.4-25mdk 
- Rebuild

* Wed Mar 26 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.2.4-24mdk
- oops, removed zcmp, zmore and zdiff from package

* Fri Mar 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.2.4-23mdk
- reintroduced, merged patches from redhat and cleaned up
- added zcmp, zmore and zdiff to package
- added some docs

* Sat Aug 11 2001 Jesse Kuang <kjx@mandrakesoft.com> 4.2.4-22mdk
- rebuilt for cooker

* Sun Sep 24 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.2.4-21mdk
- rebuilt for macros.
- use of spec helper.
- the Big Move.

* Fri Apr 14 2000 Vincent Saugey <vince@mandrakesoft.com> 4.2.4-20mdk
- corrected group

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 4.2.4-19mdk
- Added PPC Support

* Wed Nov 10 1999 Jerome Martin <jerome@mandrakesoft.com>
- minor specfile cleanup
- rebuild for new environment

* Sun Oct 31 1999 David BAUDENS <baudens@mandrakesoft.com>
- Add i486 and i686 arch (forgotten by Lord DarkChmou ;)

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix build mutliple archichtechtures..

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- build on armv4l too
- build for 6.0

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
