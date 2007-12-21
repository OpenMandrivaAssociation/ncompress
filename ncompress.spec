%define	name	ncompress
%define	oname	compress
%define	version	4.2.4
%define	release	%mkrel 34

Summary:	Fast compression and decompression utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Archiving/Compression
URL:		ftp://sunsite.unc.edu/pub/Linux/utils/compress/
Source:		ftp://sunsite.unc.edu/pub/Linux/utils/compress/%{name}-%{version}.tar.bz2
Patch0:		ncompress-4.2.4-make.patch.bz2
Patch1:		ncompress-4.2.4-lfs2.patch.bz2
Patch2:		ncompress-4.2.4-filenamelen.patch.bz2
Patch3:		ncompress-2GB.patch.bz2
Patch4:		ncompress-4.2.4-zerobyteforce.patch
Patch5: 	ncompress-4.2.4-bssUnderflow.patch
Patch6: 	ncompress-4.2.4-endians.patch

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
%patch1 -p1 -b .lfs
%patch2 -p1 -b .filenamelen
%patch3 -p1 -b .2gb
%patch4 -p1 -b .zerobyteforce
%patch5 -p1 -b .bssUnderflow
%patch6 -p1 -b .endians


%build
#- extra CFLAGS
%ifarch alpha ia64
EXTRA_FLAGS="-DNOALIGN=0"
%endif
ENDIAN_FLAGS=4321

%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ENDIAN_FLAGS=1234
%endif

%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS $ARCH32_FLAGS $EXTRA_FLAGS" ENDIAN="$ENDIAN_FLAGS"

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
