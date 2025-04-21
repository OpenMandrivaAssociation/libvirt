%define _disable_ld_no_undefined 1
%define _disable_lto 1

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
%global __requires_exclude devel\\(libxenstore.*\\)

# Assorted violations in src/util
%global optflags %{optflags} -fno-strict-aliasing -Wno-error=cpp

# enable\disable plugins
%ifarch %{ix86} %{x86_64}
%bcond_with xen
%else
%bcond_with xen
%endif
%bcond_without lxc
%bcond_without vbox
%bcond_without esx
%bcond_with hyperv
%bcond_without vmware
%bcond_without parallels

# Force QEMU to run as non-root
%define qemu_user  qemu
%define qemu_group  qemu

#define snapshot 20240529

Summary:	Toolkit to %{common_summary}
Name:		libvirt
Version:	11.2.0
Release:	%{?snapshot:0.%{snapshot}.}2
License:	LGPLv2+
Group:		System/Kernel and hardware
Url:		https://libvirt.org/
%if 0%{!?snapshot:1}
Source0:	https://libvirt.org/sources/%{name}-%{version}.tar.xz
%else
Source0:	https://gitlab.com/libvirt/libvirt/-/archive/38c6c364088e3ba2d7e0b18690af6800d338c6a9/libvirt-38c6c364088e3ba2d7e0b18690af6800d338c6a9.tar.bz2
# Commit hash for keycodemapdb must match the one seen at
# https://gitlab.com/libvirt/libvirt/-/tree/master/subprojects?ref_type=heads
Source1:	https://gitlab.com/keycodemap/keycodemapdb/-/archive/22b8996dba9041874845c7446ce89ec4ae2b713d/keycodemapdb-22b8996dba9041874845c7446ce89ec4ae2b713d.tar.bz2
%endif
Source2:	%{name}-tmpfiles.conf

BuildRequires:	cmake
BuildRequires:	dmidecode
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
BuildRequires:	iscsi-initiator-utils
#BuildRequires:	qemu
BuildRequires:	systemtap-devel
BuildRequires:	gettext-devel
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(numa)
BuildRequires:	numactl
BuildRequires:	pcap-devel
BuildRequires:	readline-devel
%if %{with xen}
BuildRequires:	xen-devel >= 3.0.4
%endif
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libcap-ng)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:  pkgconfig(json-c)
BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libiscsi)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(libsasl2)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(netcf)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(polkit-agent-1) polkit
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(xmlrpc)
BuildRequires:	pkgconfig(yajl)
BuildRequires:	pkgconfig(audit)
BuildRequires:	pkgconfig(wireshark)
BuildRequires:	python3dist(docutils)
Requires:	qemu-img
BuildSystem:	meson
BuildOption:	-Dudev=enabled
BuildOption:	-Dinit_script=systemd
%if !%{with xen}
BuildOption:	-Ddriver_libxl=disabled
%endif
%if !%{with lxc}
BuildOption:	-Ddriver_lxc=disabled
%endif
%if !%{with vbox}
BuildOption:	-Ddriver_vbox=disabled
%endif
%if !%{with esx}
BuildOption:	-Ddriver_esx=disabled
%endif
%if !%{with hyperv}
BuildOption:	-Ddriver_hyperv=disabled
%endif
%if !%{with vmware}
BuildOption:	-Ddriver_vmware=disabled
%endif
BuildOption:	-Ddriver_bhyve=disabled
BuildOption:	-Ddriver_vz=disabled
BuildOption:	-Dglusterfs=disabled
BuildOption:	-Dsanlock=disabled
BuildOption:	-Dstorage_gluster=disabled
BuildOption:	-Dopenwsman=disabled
BuildOption:	-Dnss=enabled
BuildOption:	-Djson_c=enabled
BuildOption:	-Dpolkit=enabled
BuildOption:	-Dapparmor=disabled
BuildOption:	-Drpath=disabled
BuildOption:	-Dsecdriver_apparmor=disabled
BuildOption:	-Dapparmor_profiles=disabled
BuildOption:	-Dstorage_rbd=disabled
BuildOption:	-Dstorage_vstorage=disabled
BuildOption:	-Dstorage_zfs=disabled
BuildOption:	-Dnumad=disabled
BuildOption: 	-Dnbdkit=disabled
BuildOption:  	-Dnbdkit_config_default=disabled
BuildOption:  	-Dwireshark_dissector=disabled

# add userspace tools here because the full path to each tool is hard coded into the libvirt.so* library.
BuildRequires:	dmsetup dnsmasq-base ebtables iproute2 iptables kmod lvm2 iscsi-initiator-utils parted polkit radvd systemd

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
Summary:	A library to %{common_summary}
Group:		System/Libraries

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
Requires:	qemu-kvm

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
%ifarch %{ix86} %{x86_64}
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
Summary:	Server side daemon & driver required to run LXC guests
Group:		Development/Libraries
Requires:	libvirt = %{version}-%{release}
Requires:	systemd-container

%description daemon-lxc
Server side daemon and driver required to manage the virtualization
capabilities of LXC
%endif

%prep -a
%if 0%{?snapshot:1}
# Deal with the git submodule
rmdir subprojects/keycodemapdb
cd subprojects
tar xf %{S:1}
mv keycodemapdb-* keycodemapdb
%endif

%conf -p
export SOURCE_DATE_EPOCH=$(stat --printf='%Y' %{__file_name})

%install -a
rm -f %{buildroot}%{_initrddir}/libvirt-guests

install -D -p -m 0644 %{S:2} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 %{buildroot}%{_var}/lib/%{name}
%find_lang %{name}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-libvirt.preset << EOF
enable libvirtd.service
enable virtlockd.socket
EOF

%check
#if ! make check VIR_TEST_DEBUG=1
#then
#  cat test-suite.log || true
#  #exit 1
#fi

%pre -n %{name}-utils
# 'libvirt' group is just to allow password-less polkit access to
# libvirtd. The uid number is irrelevant, so we use dynamic allocation
# described at the above link.
getent group libvirt >/dev/null || groupadd -r libvirt
exit 0

%post -n %{name}-utils
#_tmpfilescreate %{name}
%_post_service libvirtd
%_post_service libvirt-guests
%_post_service virtlockd

%preun -n %{name}-utils
%_preun_service libvirt-guests
%_preun_service libvirtd
%_preun_service virtlockd

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
#doc %{_datadir}/gtk-doc/html/%{name}
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
%{_bindir}/*
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-admin.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1.*
%{_mandir}/man1/virt-qemu-qmp-proxy.1*
%{_mandir}/man1/virt-qemu-sev-validate.1*
%{_mandir}/man8/libvirtd.8.*
%{_mandir}/man1/virt-host-validate.1.*
%{_mandir}/man1/virt-login-shell.1.*
%{_mandir}/man1/virt-qemu-run.1.*
%{_mandir}/man8/libvirt-guests.8.*
%{_mandir}/man1/virt-pki-query-dn.1.*
%{_mandir}/man8/virt-ssh-helper.8.*
%{_mandir}/man8/virtlockd.8.*
%{_mandir}/man8/virtlogd.8.*
%{_mandir}/man7/virkey*.7.*
%{_mandir}/man8/virtinterfaced.8.*
%{_mandir}/man8/virtlxcd.8.*
%{_mandir}/man8/virtnetworkd.8.*
%{_mandir}/man8/virtnodedevd.8.*
%{_mandir}/man8/virtnwfilterd.8.*
%{_mandir}/man8/virtproxyd.8.*
%{_mandir}/man8/virtqemud.8.*
%{_mandir}/man8/virtsecretd.8.*
%{_mandir}/man8/virtstoraged.8.*
%{_mandir}/man8/virtvboxd.8.*

%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%{_libexecdir}/libvirt_iohelper
%{_libexecdir}/libvirt_leaseshelper
%{_libexecdir}/libvirt_lxc
%{_libexecdir}/libvirt_parthelper
%{_libexecdir}/libvirt-guests.sh
%{_libexecdir}/libvirt-ssh-proxy
%{_prefix}/lib/firewalld/policies/libvirt-*.xml
%{_prefix}/lib/firewalld/zones/*.xml
%{_prefix}/lib/sysctl.d/60-qemu-postcopy-migration.conf
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
%{_libdir}/libvirt/connection-driver/libvirt_driver_ch.so
#{_libdir}/wireshark/epan/libvirt.so
%{_datadir}/bash-completion/completions/virsh
%{_datadir}/bash-completion/completions/virt-admin
%if %{with xen}
%{_libdir}/libvirt/connection-driver/libvirt_driver_xen.so
%{_libdir}/libvirt/connection-driver/libvirt_driver_libxl.so
%endif
%{_libdir}/libvirt/lock-driver/lockd.so
%{_var}/lib/libvirt
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/polkit-1/rules.d/50-libvirt.rules
#{_unitdir}/virtproxyd-tcp.socket
#{_unitdir}/virtproxyd-tls.socket
%{_unitdir}/virtinterfaced.service
%{_unitdir}/virtinterfaced.socket
%{_unitdir}/virtinterfaced-ro.socket
%{_unitdir}/virtinterfaced-admin.socket
%{_unitdir}/virtnetworkd.service
%{_unitdir}/virtnetworkd.socket
%{_unitdir}/virtnetworkd-ro.socket
%{_unitdir}/virtnetworkd-admin.socket
%{_unitdir}/virtnodedevd.service
%{_unitdir}/virtnodedevd.socket
%{_unitdir}/virtnodedevd-ro.socket
%{_unitdir}/virtnodedevd-admin.socket
%{_unitdir}/virtnwfilterd.service
%{_unitdir}/virtnwfilterd.socket
%{_unitdir}/virtnwfilterd-ro.socket
%{_unitdir}/virtnwfilterd-admin.socket
%{_unitdir}/virtsecretd.service
%{_unitdir}/virtsecretd.socket
%{_unitdir}/virtsecretd-ro.socket
%{_unitdir}/virtsecretd-admin.socket
%{_unitdir}/virtstoraged.service
%{_unitdir}/virtstoraged.socket
%{_unitdir}/virtstoraged-ro.socket
%{_unitdir}/virtstoraged-admin.socket
%{_unitdir}/virtqemud.service
%{_unitdir}/virtqemud.socket
%{_unitdir}/virtqemud-ro.socket
%{_unitdir}/virtqemud-admin.socket
%{_unitdir}/virtlxcd.service
%{_unitdir}/virtlxcd.socket
%{_unitdir}/virtlxcd-ro.socket
%{_unitdir}/virtlxcd-admin.socket
%if %{with xen}
%{_unitdir}/virtxend.service
%{_unitdir}/virtxend.socket
%{_unitdir}/virtxend-ro.socket
%{_unitdir}/virtxend-admin.socket
%endif
%{_unitdir}/virtvboxd.service
%{_unitdir}/virtvboxd.socket
%{_unitdir}/virtvboxd-ro.socket
%{_unitdir}/virtvboxd-admin.socket
%{_unitdir}/virtproxy*
%{_unitdir}/virtchd*
%{_libexecdir}/virt-login-shell-helper

%{_datadir}/augeas
%{_datadir}/%{name}
%{_datadir}/systemtap/tapset/libvirt_functions.stp
%{_datadir}/systemtap/tapset/libvirt_probes.stp
%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp

%config(noreplace) %{_sysconfdir}/libvirt
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace) %{_sysconfdir}/ssh/ssh_config.d/30-libvirt-ssh-proxy.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd*
%config(noreplace) %{_prefix}/lib/sysctl.d/60-libvirtd.conf
%{_presetdir}/86-libvirt.preset
%{_unitdir}/libvirtd.service
%{_unitdir}/libvirt-guests.service
%{_unitdir}/virt-guest-shutdown.target
%{_unitdir}/virtlockd*.*
%{_unitdir}/virtlogd*.*
%{_unitdir}/libvirtd.socket
%{_unitdir}/libvirtd-ro.socket
%{_unitdir}/libvirtd-admin.socket
%{_unitdir}/libvirtd-tcp.socket
%{_unitdir}/libvirtd-tls.socket
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/*.conf
