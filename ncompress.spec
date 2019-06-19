%define	oname	compress

Summary:	Fast compression and decompression utilities
Name:		ncompress
Version:	4.2.4.5
Release:	12
License:	Public Domain
Group:		Archiving/Compression
Url:		http://ncompress.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ncompress/%{name}-%{version}.tar.gz
Patch0:		ncompress-4.2.4-make.patch
Patch1:		ncompress-4.2.4-lfs2.patch
Patch2:		ncompress-4.2.4.2-filenamelen.patch
Patch3:		ncompress-2GB.patch
Patch6:		ncompress-4.2.4-endians.patch
Patch7:		ncompress-4.2.4.2-LDFLAGS.diff

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
install -m755 %{oname} -D %{buildroot}%{_bindir}/%{oname}
ln -sf %{oname} %{buildroot}%{_bindir}/uncompress
install -m644 %{oname}.1 -D %{buildroot}%{_mandir}/man1/%{oname}.1
ln -sf %{oname}.1.bz2 %{buildroot}%{_mandir}/man1/uncompress.1.bz2

%files
%doc LZW.INFO README Changes Acknowleds
%{_bindir}/*
%{_mandir}/man1/*

