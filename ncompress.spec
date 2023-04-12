%define oname compress

Summary:	Fast compression and decompression utilities
Name:		ncompress
Version:	5.0
Release:	3
License:	Public Domain
Group:		Archiving/Compression
Url:		https://github.com/vapier/ncompress
Source0:	https://github.com/vapier/ncompress/archive/%{name}-%{version}.tar.gz
# allow to build ncompress
# ~> downstream
Patch0:	https://src.fedoraproject.org/rpms/ncompress/raw/rawhide/f/ncompress-5.0-make.patch

# from dist-git commit 0539779d937
# (praiskup: removed redundant part as -DNOFUNCDEF is defined)
# ~> downstream
Patch1:	https://src.fedoraproject.org/rpms/ncompress/raw/rawhide/f/ncompress-5.0-lfs.patch

# permit files > 2GB to be compressed
# ~> #126775
Patch3:	https://src.fedoraproject.org/rpms/ncompress/raw/rawhide/f/ncompress-5.0-2GB.patch

# do not fail to compress on ppc/s390x
# ~> #207001
Patch4:	https://src.fedoraproject.org/rpms/ncompress/raw/rawhide/f/ncompress-5.0-endians.patch

# use memmove instead of memcpy
# ~> 760657
# ~> downstream
Patch5:	https://src.fedoraproject.org/rpms/ncompress/raw/rawhide/f/ncompress-5.0-memmove.patch

%description
The ncompress package contains the compress and uncompress
file compression and decompression utilities, which are compatible
with the original UNIX compress utility (.Z file extensions).  These
utilities can't handle gzipped (.gz file extensions) files, but
gzip can handle compressed files.

%prep
%autosetup -p2

%build
%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ARCH_FLAGS="$ARCH_FLAGS -DBYTEORDER=1234"
%endif

%ifarch alpha ia64
ARCH_FLAGS="$ARCH_FLAGS -DNOALLIGN=0"
%endif

%make_build CFLAGS="%{optflags}" ARCH_FLAGS="$ARCH_FLAGS" LDFLAGS="%{build_ldflags}"

%install
install -m755 %{oname} -D %{buildroot}%{_bindir}/%{oname}
ln -sf %{oname} %{buildroot}%{_bindir}/uncompress
install -m644 %{oname}.1 -D %{buildroot}%{_mandir}/man1/%{oname}.1
ln -sf %{oname}.1 %{buildroot}%{_mandir}/man1/uncompress.1

%files
%doc LZW.INFO Changes Acknowleds
%{_bindir}/*
%doc %{_mandir}/man1/*
