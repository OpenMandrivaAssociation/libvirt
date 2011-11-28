%define common_summary interact with virtualization capabilities
%define common_description Libvirt is a C toolkit to interact with the virtualization\
capabilities of recent versions of Linux.
%define lib_major 0

%define lib_name %mklibname virt %{lib_major}
%define develname %mklibname -d virt
%define staticdevelname %mklibname -d -s virt

# libxenstore is not versionned properly
%define _requires_exceptions devel(libxenstore.*)

Name:       libvirt
Version:    0.9.7
Release:    %mkrel 1
Summary:    Toolkit to %{common_summary}
License:    LGPLv2+
Group:      System/Kernel and hardware
Url:        http://libvirt.org/
Source:     http://libvirt.org/sources/%{name}-%{version}.tar.gz
# XXX: for %%{_sysconfdir}/sasl2
Requires:   cyrus-sasl
%ifarch %{ix86} x86_64
BuildRequires:  xen-devel >= 3.0.4
%endif
BuildRequires:  libxml2-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  python-devel
BuildRequires:  gnutls-devel
BuildRequires:  libsasl-devel
BuildRequires:  libpciaccess-devel
%if %{mdkversion} >= 201000
BuildRequires:  polkit-1-devel
%else
BuildRequires:  polkit-devel
%endif
BuildRequires:  parted-devel
BuildRequires:  open-iscsi
BuildRequires:  lvm2
BuildRequires:  dmsetup
BuildRequires:  libxml2-utils
BuildRequires:  nfs-utils 
BuildRequires:  libavahi-client-devel
BuildRequires:  xmlrpc-c-devel
%if %{mdkversion} >= 201000
BuildRequires:  numa-devel
%endif
BuildRequires:  qemu
BuildRequires:  gettext-devel
BuildRequires:  libnl-devel
BuildRequires:  libpcap-devel
BuildRequires:  systemtap
%if %{mdkversion} >= 201010
BuildRequires:	netcf-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
%{common_description}

Virtualization of the Linux Operating System means the
ability to run multiple instances of Operating Systems concurently on
a single hardware system where the basic resources are driven by a
Linux instance. The library aim at providing long term stable C API
initially for the Xen paravirtualization but should be able to
integrate other virtualization mechanisms if needed.

%package -n %{lib_name}
Summary:    A library to %{common_summary}
Group:      System/Libraries

%description -n %{lib_name}
%{common_description}

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:    Development tools for programs using %{name}
Group:      Development/C
Requires:   %{lib_name} = %{version}
%ifarch %{ix86} x86_64
Requires:   xen-devel
%endif
Provides:   %{name}-devel = %{version}-%{release}
Obsoletes:  %{lib_name}-devel

%description -n %{develname}
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package -n %{staticdevelname}
Summary:    Development static libraries for programs using %{name}
Group:      Development/C
Provides:   %{name}-static-devel = %{version}-%{release}
Obsoletes:  %{lib_name}-static-devel

%description -n %{staticdevelname}
%{common_description}

This package contains the static libraries needed for developing
programs using the %{name} library.

%package -n python-%{name}
Summary:    Python bindings to %{common_summary}
Group:      Development/Python

%description -n python-%{name}
%{common_description}

This package contains the python bindings for the %{name} library.

%package -n %{name}-utils
Summary:    Tools to %{common_summary}
Group:      System/Kernel and hardware
Requires:   bridge-utils
Requires:   %{lib_name} = %{version}
%if %{mdkversion} >= 201000
Requires:   polkit
%else
Requires:   policykit
%endif
Suggests:   dnsmasq-base
Suggests:   netcat-openbsd
Conflicts:  libvirt0 < 0.7.1-2
Conflicts:  lib64virt0 < 0.7.1-2

%description -n %{name}-utils
%{common_description}

This package contains tools for the %{name} library.

%prep
%setup -q

%build
%configure2_5x \
    --localstatedir=%{_var}  \
    --with-html-subdir=%{name} \
    --with-udev \
    --without-hal
%make

%install
rm -rf %{buildroot}
%makeinstall_std
install -d -m 755 %{buildroot}%{_var}/run/%{name}
install -d -m 755 %{buildroot}%{_var}/lib/%{name}
%find_lang %{name}

# fix documentation
mv %{buildroot}%{_docdir}/%{name}-python-%{version} %{buildroot}%{_docdir}/python-%{name}
install -m 644 ChangeLog README TODO NEWS %{buildroot}%{_docdir}/%{name}

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{py_platsitedir}/*.la

%check
# fhimpe: disabled for now because it fails on 100Hz kernels, such as used on bs
# http://www.mail-archive.com/libvir-list@redhat.com/msg13727.html
#make check

%clean
rm -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/%{name}.so.%{lib_major}*
%{_libdir}/%{name}-qemu.so.%{lib_major}*

%files -n %{develname}
%defattr(-,root,root)
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/ChangeLog
%exclude %{_docdir}/%{name}/README
%exclude %{_docdir}/%{name}/TODO
%exclude %{_docdir}/%{name}/NEWS
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/%{name}-qemu.so
%{_libdir}/libvirt_lxc
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/%{name}.a
%{_libdir}/%{name}-qemu.a

%files -n python-%{name}
%defattr(-,root,root)
%doc %{_docdir}/python-%{name}
%{py_platsitedir}/%{name}.py
%{py_platsitedir}/%{name}mod.so

%files -n %{name}-utils -f %{name}.lang
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/README
%{_docdir}/%{name}/TODO
%{_docdir}/%{name}/NEWS
%{_bindir}/*
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1.*
%{_mandir}/man8/libvirtd.8.*
%{_sbindir}/*
%{_initrddir}/libvirtd
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/uml/
%{_libdir}/libvirt_iohelper
%{_libdir}/libvirt_parthelper
%{_var}/run/libvirt
%{_var}/lib/libvirt
%if %{mdkversion} >= 201000
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%else
%{_datadir}/PolicyKit/policy/org.libvirt.unix.policy
%endif
%{_datadir}/augeas
%{_datadir}/%{name}
%{_datadir}/systemtap/tapset/libvirtd.stp
%config(noreplace) %{_sysconfdir}/libvirt
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/libvirt-guests
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd*
%{_initrddir}/libvirt-guests
%{py_platsitedir}/libvirt_qemu.py
%{py_platsitedir}/libvirtmod_qemu.so

