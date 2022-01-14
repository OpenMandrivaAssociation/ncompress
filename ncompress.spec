%define	oname	compress

Summary:	Fast compression and decompression utilities
Name:		ncompress
Version:	5.0
Release:	1
License:	Public Domain
Group:		Archiving/Compression
Url:		https://github.com/vapier/ncompress
Source0:	https://github.com/vapier/ncompress/archive/%{name}-%{version}.tar.gz

%description
The ncompress package contains the compress and uncompress
file compression and decompression utilities, which are compatible
with the original UNIX compress utility (.Z file extensions).  These
utilities can't handle gzipped (.gz file extensions) files, but
gzip can handle compressed files.

%prep
%autosetup -p1

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
%doc LZW.INFO Changes Acknowleds
%{_bindir}/*
%{_mandir}/man1/*

