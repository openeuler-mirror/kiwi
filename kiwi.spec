%{?python_enable_dependency_generator}

Name:           kiwi
Version:        9.16.12
Release:        3
License:        GPLv3+
Summary:        Flexible operating system image builder

URL:            http://suse.github.io/kiwi/
Source0:        https://files.pythonhosted.org/packages/source/k/%{name}/%{name}-%{version}.tar.gz

#Patch1000 comes from Fedora 29
Patch1000:      kiwi-9.12.8-use-pyxattr.patch

BuildRequires:  bash-completion dracut fdupes gcc make
%if %{with_python2}
BuildRequires:  python2-devel python2-setuptools
%endif
BuildRequires:  python3-devel python3-setuptools shadow-utils

BuildRequires:  %{_bindir}/sphinx-build-3 python3-sphinxcontrib-spelling 
BuildRequires:  python3-docopt python3-future python3-lxml python3-pyxattr
BuildRequires:  python3-six python3-pyyaml python3-requests

%description 
KIWI is an imaging solution that is based on an image XML description.
Such a description is represented by a directory which includes at least
one config.xml or .kiwi file and may as well include other files like 
scripts or configuration data.

%package 	systemdeps
Summary:        Common system dependencies for %{name}
Provides:       %{name}-image:docker %{name}-image:iso %{name}-image:oem
Provides:       %{name}-image:pxe %{name}-image:tbz %{name}-image:vmx

Requires:       dnf
Provides:       %{name}-packagemanager:dnf

Requires:       yum
Provides:       %{name}-packagemanager:yum

Requires:       device-mapper-multipath dosfstools e2fsprogs
Requires:       xorriso gdisk grub2 lvm2 mtools parted
Requires:       qemu-img rsync squashfs-tools tar >= 1.2.7
Requires:       %{name}-tools = %{version}-%{release}

Recommends:     debootstrap jing

%ifarch %{arm} aarch64
Requires:       uboot-tools
%endif
%ifarch x86_64
Requires:       grub2-efi
%endif
%if ! %{with_python2}
Obsoletes:      python2-%{name} < %{version}-%{release}
%endif

%description 	systemdeps
This metapackage installs the necessary system dependencies
to run KIWI.

%if %{with_python2}
%package 	-n python2-%{name}
Summary:        %{name} - Python 2 implementation
Requires:       %{name}-systemdeps = %{version}-%{release}
Requires:       python2-setuptools

Conflicts:      flumotion < 0.11.0.1-9
BuildArch:      noarch
%{?python_provide:%python_provide python2-%{name}}

%description 	-n python2-%{name}
Python 2 package of the %{name}. Provides an operating system
image builder for Linux supported hardware platforms and for
virtualization,such as Xen, KVM, VMware, EC2 and so on.
%endif

%package 	-n python3-%{name}
Summary:        %{name} - Python 3 implementation
Requires:       %{name}-systemdeps = %{version}-%{release}
Requires:       python3-setuptools
BuildArch:      noarch
%{?python_provide:%python_provide python3-%{name}}

%description 	-n python3-%{name}
Python 3 package of the %{name}. Provides an operating system
image builder for Linux supported hardware platforms and for
virtualization,such as Xen, KVM, VMware, EC2 and so on.

%package 	tools
Summary:        Tools for boot

%description 	tools
%{name}-tools package contains some helper tools,which is used for the
%{name} created initial ramdisk used to control the very first boot of 
an appliance.

%ifarch %{ix86} x86_64
%package 	pxeboot
Summary:        %{name} - PXE boot structure
Requires:       syslinux
Requires:       tftp-server

%description 	pxeboot
%{name}-pxeboot package contains the basic PXE directory structure which is
needed to serve %{name} built images via PXE.
%endif

%package 	cli
Summary:        Flexible operating system appliance image builder
Provides:       %{name}-schema = 6.9
Provides:       %{name} = %{version}-%{release}
Requires:       python3-%{name} = %{version}-%{release}
Requires:       bash-completion
BuildArch:      noarch

%description 	cli 
%{name} is an imaging solution that is based on an image XML description.
Such a description is represented by a directory which includes at least
one config.xml or .kiwi file and may as well include other files like 
scripts or configuration data.

%package 	other
Summary:        Other information about %{name}
Requires:       bc btrfs-progs coreutils cryptsetup curl device-mapper
Requires:       dialog dracut e2fsprogs gdisk grep lvm2 mdadm parted
Requires:       pv util-linux xfsprogs xz xorriso
Requires:       device-mapper-multipath gawk kexec-tools
BuildArch:      noarch

Provides:       dracut-%{name}-lib dracut-%{name}-oem-repart dracut-%{name}-oem-dump
Provides:       dracut-%{name}-oem-dump dracut-%{name}-live

Obsoletes:      dracut-%{name}-lib dracut-%{name}-oem-repart dracut-%{name}-oem-dump
Obsoletes:      dracut-%{name}-oem-dump dracut-%{name}-live

%description 	other
%{name}-other package contains other information about %{name}.


%package_help

%prep
%autosetup -n %{name}-%{version} -p1

sed -e "s|#!/usr/bin/env python||" -i kiwi/xml_parse.py

%build
%set_build_flags

%make_build -C doc man SPHINXBUILD=sphinx-build-3

%if %{with_python2}
%py2_build
%endif
%py3_build

%install
%if %{with_python2}
%py2_install
%endif
%py3_install

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mv %{buildroot}%{_sysconfdir}/bash_completion.d/kiwi-ng-3.sh %{buildroot}%{_datadir}/bash-completion/completions/kiwi-ng

rm -rf %{buildroot}%{_sysconfdir}/bash_completion.d

rm -rf %{buildroot}%{_docdir}/packages

ln -sr %{buildroot}%{_bindir}/kiwi-ng %{buildroot}%{_bindir}/kiwi
ln -sr %{buildroot}%{_bindir}/kiwi-ng-3 %{buildroot}%{_bindir}/kiwi-ng
ln -sr %{buildroot}%{_bindir}/kiwicompat-3 %{buildroot}%{_bindir}/kiwicompat

%ifarch %{ix86} x86_64
for i in KIWI pxelinux.cfg image upload boot; do \
    mkdir -p %{buildroot}%{_sharedstatedir}/tftpboot/$i ;\
done
%fdupes %{buildroot}%{_sharedstatedir}/tftpboot
%endif

%files systemdeps

%if %{with_python2}
%files -n python2-%{name}
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}*
%{python2_sitelib}/%{name}*/
%endif

%files -n python3-%{name}
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}*
%{python3_sitelib}/%{name}*/

%files tools
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%exclude %{_bindir}/kiwi-ng-2
%exclude %{_bindir}/kiwicompat-2

%files cli
%defattr(-,root,root)
%{_bindir}/%{name}*
%{_datadir}/bash-completion/completions/%{name}-ng

%ifarch %{ix86} x86_64
%files pxeboot
%defattr(-,root,root)
%license LICENSE
%{_sharedstatedir}/tftpboot/*
%endif

%files other
%defattr(-,root,root)
%license LICENSE
%{_prefix}/lib/dracut/modules.d/*

%files help
%defattr(-,root,root)
%{_mandir}/man8/%{name}*

%changelog
* Thu Feb 27 2020 lijin Yang <yanglijin@huawei.com> - 9.16.12-3
- Remove python2 dependency

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 9.16.12-2
- Package init
