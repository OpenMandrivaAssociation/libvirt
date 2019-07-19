%define _disable_ld_no_undefined 1
%define _disable_lto 1

%global optflags %{optflags}
#--rtlib=compiler-rt

%define common_summary interact with virtualization capabilities
%define common_description Libvirt is a C toolkit to interact with the virtualization\
capabilities of recent versions of Linux.

%define major 0
%define libname %mklibname virt %{major}
%define libadmin %mklibname virt-admin %{major}
%define libqemu %mklibname virt-qemu %{major}
%define liblxc %mklibname virt-lxc %{major}
%define devname %mklibname -d virt

# libxenstore is not versionned properly
%define __noautoreq 'devel(libxenstore.*)'


# enable\disable plugins
%ifarch %{ix86} x86_64
%bcond_with	xen
%else
%bcond_with	xen
%endif
%bcond_without	lxc
%bcond_without	vbox
%bcond_without	esx
%bcond_without	hyperv
%bcond_without	vmware
%bcond_without	parallels


Summary:	Toolkit to %{common_summary}
Name:		libvirt
Version:	5.5.0
Release:	1
License:	LGPLv2+
Group:		System/Kernel and hardware
Url:		http://libvirt.org/
Source0:	http://libvirt.org/sources/%{name}-%{version}.tar.xz
Source1:	%{name}-tmpfiles.conf
#Patch0:		libvirt-1.2.3-mga-no-daemonize.patch
#Patch0:		libvirt-3.9.0-clang.patch
Patch203:	rpcgen-libvirt-1.1.2.patch

BuildRequires:	docbook-style-xsl
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(devmapper)
BuildRequires:	dmsetup
BuildRequires:	libxml2-utils
BuildRequires:	lvm2
BuildRequires:	glibc-devel
BuildRequires:	nfs-utils
BuildRequires:	open-iscsi
#BuildRequires:	qemu
BuildRequires:	systemtap-devel
BuildRequires:	gettext-devel
BuildRequires:	sasl-devel
%ifnarch %arm %mips aarch64
BuildRequires:	numa-devel
BuildRequires:	numactl
%endif
BuildRequires:	pcap-devel
BuildRequires:	readline-devel
%if %{with xen}
BuildRequires:	xen-devel >= 3.0.4
%endif
BuildRequires:	xsltproc
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
BuildRequires: 	pkgconfig(systemd)
BuildRequires: 	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(xmlrpc)
BuildRequires:	pkgconfig(yajl)

# add userspace tools here because the full path to each tool is hard coded into the libvirt.so* library.
BuildRequires:  dmsetup dnsmasq-base ebtables iproute2 iptables kmod lvm2 open-iscsi parted polkit radvd systemd

Requires:	cyrus-sasl
Requires:	gettext
Requires:	netcf

%description
%{common_description}

Virtualization of the Linux Operating System means the
ability to run multiple instances of Operating Systems concurently on
a single hardware system where the basic resources are driven by a
Linux instance. The library aim at providing long term stable C API
initially for the Xen paravirtualization but should be able to
integrate other virtualization mechanisms if needed.

%package -n %{libadmin}
Summary:        A library to %{common_summary}
Group:          System/Libraries

%description -n %{libadmin}
This package contains the library needed to run programs dynamically
linked with %{name}.

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
%if %{with xen}
%ifarch %{ix86} x86_64
Requires:	xen-devel
%endif
%endif
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package -n %{name}-utils
Summary:	Tools to %{common_summary}
Group:		System/Kernel and hardware
Requires:	bridge-utils
Requires:	polkit
Requires:	ebtables
Requires:	netcf
Requires:	dnsmasq-base
Suggests:	netcat-openbsd
Conflicts:	%{_lib}virt0 < 1.0.1-1

%description -n %{name}-utils
%{common_description}

This package contains tools for the %{name} library.


%if %{with lxc}
%package daemon-lxc
Summary: Server side daemon & driver required to run LXC guests
Group: Development/Libraries
Requires: libvirt = %{version}-%{release}
Requires: systemd-container

%description daemon-lxc
Server side daemon and driver required to manage the virtualization
capabilities of LXC
%endif

%prep
%setup -q
%apply_patches

%build
# not working with clang
export CC=gcc
export CXX=g++
autoreconf -fi
%configure \
	--disable-static \
	--localstatedir=%{_var}  \
	--with-html-subdir=%{name} \
	--with-udev \
	--with-init_script=systemd \
	%if !%{with xen}
	--without-xenapi \
	%endif
	%if !%{with lxc}
	--without-lxc \
	%endif
	%if !%{with vbox}
	--without-vbox \
	%endif
	%if !%{with esx}
	--without-esx \
	%endif
	%if !%{with hyperv}
	--without-hyperv \
	%endif
	%if !%{with vmware}
	--without-vmware \
	%endif
	%if !%{with parallels}
	--without-parallels \
	%endif
	--without-hal \
	--with-systemd-daemon \
	--with-udev \
	--with-polkit \
	--with-avahi

%make_build LIBS="-ltirpc -ldl"

%install
%make_install SYSTEMD_UNIT_DIR=%{_unitdir}

rm -f %{buildroot}%{_initrddir}/libvirt-guests
find %{buildroot} -name '*.la' -delete

install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 %{buildroot}%{_var}/lib/%{name}
%find_lang %{name}

# fix documentation
install -m 644 ChangeLog README NEWS %{buildroot}%{_docdir}/%{name}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-libvirt.preset << EOF
enable libvirtd.service
enable virtlockd.socket
EOF

%check
# fhimpe: disabled for now because it fails on 100Hz kernels, such as used on bs
# http://www.mail-archive.com/libvir-list@redhat.com/msg13727.html
#make check

%post -n %{name}-utils
#_tmpfilescreate %{name}
%_post_service  libvirtd
%_post_service  libvirt-guests
%_post_service	virtlockd

%preun -n %{name}-utils
%_preun_service libvirt-guests
%_preun_service libvirtd
%_preun_service	virtlockd

%libpackage nss_libvirt 2
%libpackage nss_libvirt_guest 2

%files -n %{libadmin}
%{_libdir}/%{name}-admin.so.%{major}*

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
%exclude %{_docdir}/%{name}/NEWS
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/%{name}-admin.so
%{_libdir}/%{name}-qemu.so
%{_libdir}/%{name}-lxc.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-qemu.pc
%{_libdir}/pkgconfig/%{name}-lxc.pc
%{_libdir}/pkgconfig/%{name}-admin.pc

%files -n %{name}-utils -f %{name}.lang
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/README
%{_docdir}/%{name}/NEWS
%{_bindir}/*
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-admin.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1.*
%{_mandir}/man8/libvirtd.8.*
%{_mandir}/man1/virt-host-validate.1.*
%{_mandir}/man1/virt-login-shell.1.*
%{_mandir}/man8/virtlockd.8.xz
%{_mandir}/man8/virtlogd.8.xz
%{_mandir}/man7/virkey*.7.xz
%{_sbindir}/*
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%{_libexecdir}/libvirt_iohelper
%{_libexecdir}/libvirt_leaseshelper
%{_libexecdir}/libvirt_lxc
%{_libexecdir}/libvirt_parthelper
%{_libexecdir}/libvirt-guests.sh
%{_prefix}/lib/firewalld/zones/libvirt.xml
%{_libdir}/libvirt/connection-driver/libvirt_driver_interface.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_network.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_secret.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_storage.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox.so
%{_libdir}/libvirt/storage-backend/libvirt_storage_*.so
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%if %{with xen}
%{_libdir}/libvirt/connection-driver/libvirt_driver_xen.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_libxl.so
%endif
%{_libdir}/libvirt/lock-driver/lockd.so
%{_var}/run/libvirt
%{_var}/lib/libvirt
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/polkit-1/rules.d/50-libvirt.rules

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
%config(noreplace) %{_sysconfdir}/sysconfig/virtlogd
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd*
%config(noreplace) %{_prefix}/lib/sysctl.d/60-libvirtd.conf
%{_presetdir}/86-libvirt.preset
%{_unitdir}/libvirtd.service
%{_unitdir}/libvirt-guests.service
%{_unitdir}/virt-guest-shutdown.target
%{_unitdir}/virtlockd*.*
%{_unitdir}/virtlogd*.*
%{_tmpfilesdir}/%{name}.conf
