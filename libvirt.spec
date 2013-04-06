%define _disable_ld_no_undefined 1

%define common_summary interact with virtualization capabilities
%define common_description Libvirt is a C toolkit to interact with the virtualization\
capabilities of recent versions of Linux.

%define major 0
%define libname %mklibname virt %{major}
%define libqemu %mklibname virt-qemu %{major}
%define liblxc %mklibname virt-lxc %{major}
%define devname %mklibname -d virt

# libxenstore is not versionned properly
%define __noautoreq 'devel(libxenstore.*)'

Summary:	Toolkit to %{common_summary}
Name:		libvirt
Version:	1.0.2
Release:	3
License:	LGPLv2+
Group:		System/Kernel and hardware
Url:		http://libvirt.org/
Source0:	http://libvirt.org/sources/%{name}-%{version}.tar.gz
Patch0:		libvirt-0.9.7-undefined_fix.diff
Patch1:		libvirt_automake.patch
Patch2:		libvirt-1.0.2_xdr_uint64_t.patch

BuildRequires:	dmsetup
BuildRequires:	libxml2-utils
BuildRequires:	lvm2
BuildRequires:	glibc-devel
BuildRequires:	nfs-utils
BuildRequires:	open-iscsi
BuildRequires:	qemu
BuildRequires:	systemtap
BuildRequires:	gettext-devel
BuildRequires:	libsasl-devel
BuildRequires:	numa-devel
BuildRequires:	pcap-devel
BuildRequires:	readline-devel
%ifarch %{ix86}	x86_64
BuildRequires:	xen-devel >= 3.0.4
%endif
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(netcf)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(polkit-agent-1) polkit
BuildRequires:	pkgconfig(python)
BuildRequires: 	pkgconfig(systemd)
BuildRequires:	pkgconfig(xmlrpc)
BuildRequires:	pkgconfig(yajl)
Requires:	cyrus-sasl

%description
%{common_description}

Virtualization of the Linux Operating System means the
ability to run multiple instances of Operating Systems concurently on
a single hardware system where the basic resources are driven by a
Linux instance. The library aim at providing long term stable C API
initially for the Xen paravirtualization but should be able to
integrate other virtualization mechanisms if needed.

%package -n %{libname}
Summary:	A library to %{common_summary}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libqemu}
Summary:	A library to %{common_summary}
Group:		System/Libraries
Conflicts:	%{_lib}virt0 < 1.0.2-1

%description -n %{libqemu}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{liblxc}
Summary:	A library to %{common_summary}
Group:		System/Libraries

%description -n %{liblxc}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{devname}
Summary:	Development tools for programs using %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	%{libqemu} = %{version}
Requires:	%{liblxc} = %{version}
%ifarch %{ix86} x86_64
Requires:	xen-devel
%endif
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package -n python-%{name}
Summary:	Python bindings to %{common_summary}
Group:		Development/Python
Conflicts:	%{name}-utils < 1.0.1-1

%description -n python-%{name}
%{common_description}

This package contains the python bindings for the %{name} library.

%package -n %{name}-utils
Summary:	Tools to %{common_summary}
Group:		System/Kernel and hardware
Requires:	bridge-utils
Requires:	polkit
Suggests:	dnsmasq-base
Suggests:	netcat-openbsd
Conflicts:	%{_lib}virt0 < 1.0.1-1

%description -n %{name}-utils
%{common_description}

This package contains tools for the %{name} library.

%prep
%setup -q
%apply_patches

%build
autoreconf -fi
%configure2_5x \
	--disable-static \
	--localstatedir=%{_var}  \
	--with-html-subdir=%{name} \
	--with-udev \
	--with-init_script=systemd \
	--without-hal

%make

%install
%makeinstall_std
install -d -m 755 %{buildroot}%{_var}/run/%{name}
install -d -m 755 %{buildroot}%{_var}/lib/%{name}
%find_lang %{name}

# fix documentation
mv %{buildroot}%{_docdir}/%{name}-python-%{version} %{buildroot}%{_docdir}/python-%{name}
install -m 644 ChangeLog README TODO NEWS %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/%{name}.so.%{major}*

%files -n %{libqemu}
%{_libdir}/%{name}-qemu.so.%{major}*

%files -n %{liblxc}
%{_libdir}/%{name}-lxc.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/ChangeLog
%exclude %{_docdir}/%{name}/README
%exclude %{_docdir}/%{name}/TODO
%exclude %{_docdir}/%{name}/NEWS
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/%{name}-qemu.so
%{_libdir}/%{name}-lxc.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_libxl.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n python-%{name}
%doc %{_docdir}/python-%{name}
%{py_platsitedir}/%{name}*.py
%{py_platsitedir}/%{name}mod*.so

%files -n %{name}-utils -f %{name}.lang
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
%{_mandir}/man1/virt-host-validate.1.*
%{_sbindir}/*
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/uml/
%{_libexecdir}/libvirt_iohelper
%{_libexecdir}/libvirt_lxc
%{_libexecdir}/libvirt_parthelper
%{_libexecdir}/libvirt-guests.sh
%{_libdir}/libvirt/connection-driver/libvirt_driver_interface.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_network.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_secret.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_storage.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_uml.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_xen.so
%{_libdir}/libvirt/lock-driver/lockd.so
%{_var}/run/libvirt
%{_var}/lib/libvirt
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/augeas
%{_datadir}/%{name}
%{_datadir}/systemtap/tapset/libvirt_functions.stp
%{_datadir}/systemtap/tapset/libvirt_probes.stp
%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp

%config(noreplace) %{_sysconfdir}/libvirt
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/libvirt-guests
%config(noreplace) %{_sysconfdir}/sysconfig/virtlockd
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd*
%config(noreplace) %{_prefix}/lib/sysctl.d/libvirtd.conf
%{_unitdir}/libvirtd.service
%{_unitdir}/libvirt-guests.service
%{_unitdir}/virtlockd.*

