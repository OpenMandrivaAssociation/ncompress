%define	name	ncompress
%define	oname	compress
%define	version	4.2.4
%define	release	%mkrel 32

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
Patch4:		ncompress-4.2.4-CVE-2006-1168.patch
Patch5:		ncompress-4.2.4-zerobyteforce.patch
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
%patch4 -p0 -b .cve-2006-1168
%patch5 -p1 -b .zerobyteforce

%build
#- check for cpu endianess
F=./ck-endian
cat > $F.c << EOF
int main(void) {
  union { long l; char c[sizeof(long)]; } u = { .l = 1 };
  return u.c[sizeof(long) - 1] == 1;
}
EOF
%__cc -o $F $F.c || exit 1
ENDIAN_FLAGS="`$F && echo 4321 || echo 1234`"

#- check for 32-bit cpus
F=./ck-arch32
echo 'int main(void) { return sizeof(void *) != 4; }' | %__cc -o $F -xc - || exit 1
$F && ARCH32_FLAGS=" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

#- extra CFLAGS
%ifarch alpha
EXTRA_FLAGS="-DNOALIGN=0"
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
