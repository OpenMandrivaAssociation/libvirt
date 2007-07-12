%define name libvirt
%define version 0.3.0
%define release %mkrel 1
%define common_summary interact with virtualization capabilities
%define common_description Libvirt is a C toolkit to interact with the virtualization\
capabilities of recent versions of Linux.
%define lib_major 0

%define lib_name %mklibname virt %{lib_major}
%define develname %mklibname -d virt
%define staticdevelname %mklibname -d -s virt

# libxenstore is not versionned properly
%define _requires_exceptions devel(libxenstore.*)

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    Toolkit to %{common_summary}
License:    LGPL
Group:      System/Kernel and hardware
Url:        http://libvirt.org/
Source0:    ftp://libvirt.org/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  xen >= 3.0.4
BuildRequires:  libxml2-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  python-devel
BuildRequires:  gnutls-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}


%description
%{common_description}

Virtualization of the Linux Operating System means the
ability to run multiple instances of Operating Systems concurently on
a single hardware system where the basic resources are driven by a
Linux instance. The library aim at providing long term stable C API
initially for the Xen paravirtualization but should be able to
integrate other virtualization mechanisms if needed.

%package -n	%{lib_name}
Summary:	A library to %{common_summary}
Group:		System/Libraries

%description -n	%{lib_name}
%{common_description}

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Development tools for programs using %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{lib_name}-devel

%description -n	%{develname}
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package -n	%{staticdevelname}
Summary:	Development static libraries for programs using %{name}
Group:		Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{lib_name}-static-devel

%description -n	%{staticdevelname}
%{common_description}

This package contains the static libraries needed for developing
programs using the %{name} library.

%package -n	python-%{name}
Summary:	Python bindings to %{common_summary}
Group:		Development/Python

%description -n	python-%{name}
%{common_description}

This package contains the python bindings for the %{name} library.

%package -n	%{name}-utils
Summary:	Tools to %{common_summary}
Group:		System/Kernel and hardware

%description -n	%{name}-utils
%{common_description}

This package contains tools for the %{name} library.


%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name} -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog README TODO NEWS
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}_proxy

%files -n %{develname}
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}
%doc %{_datadir}/gtk-doc/html/%{name}
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.la
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/%{name}.a

%files -n python-%{name}
%defattr(-,root,root)
%doc %{_docdir}/%{name}-python-%{version}
%{py_platsitedir}/%{name}.py
%{py_platsitedir}/%{name}mod.a
%{py_platsitedir}/%{name}mod.la
%{py_platsitedir}/%{name}mod.so

%files -n %{name}-utils
%defattr(-,root,root)
%{_bindir}/virsh
%{_mandir}/man1/virsh.1*
%{_sbindir}/libvirt_qemud
%{_initrddir}/libvirtd
%config(noreplace) %{_sysconfdir}/libvirt
