%{?python_enable_dependency_generator}

Name:           kiwi
Version:        9.21.5
Release:        3
License:        GPLv3+
Summary:        Flexible operating system image builder

URL:            http://osinside.github.io/kiwi/
Source0:        https://files.pythonhosted.org/packages/source/k/%{name}/%{name}-%{version}.tar.gz

Patch0:	Added-microdnf-support-in-XML-schema.patch
Patch1:	Simplify-build_status-helpe.patch
Patch2:	Include-box-plugin-images-to-build_status.patch
Patch3:	Added-s390-SLE15-integration-tests.patch
Patch4:	Cosmetic-update-for-build-status-helper.patch
Patch5:	Added-universal-box-to-build-status-helper.patch
Patch6000: 86f06b92e6d227844965d9f18e84c7da53a42b30.patch

BuildRequires:  bash-completion dracut fdupes gcc make
BuildRequires:  python3-devel python3-setuptools shadow-utils

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
Requires:       xorriso gdisk lvm2 mtools parted
Requires:       qemu-img rsync squashfs-tools tar >= 1.2.7
Requires:       %{name}-tools = %{version}-%{release}
%ifarch x86_64
Requires:       syslinux
%endif

Recommends:     debootstrap jing

%ifarch aarch64
Requires:       uboot-tools grub2-efi-aa64-modules
%endif
%ifarch x86_64
Requires:       grub2-tools-efi grub2-efi-x64-modules grub2-efi-ia32-modules grub2-pc-modules
%endif
Obsoletes:      python2-%{name} < %{version}-%{release}

%description 	systemdeps
This metapackage installs the necessary system dependencies
to run KIWI.

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
Provides:       %{name}-schema = 7.1
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
Requires:       pv util-linux xfsprogs xz xorriso parted
Requires:       gawk kexec-tools
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

%py3_build
make CFLAGS="%{build_cflags}" tools

%install
%py3_install
make buildroot=%{buildroot}/ install
make buildroot=%{buildroot}/ install_dracut

rm -rf %{buildroot}%{_sysconfdir}/bash_completion.d

rm -rf %{buildroot}%{_docdir}/packages

mv %{buildroot}%{_bindir}/kiwi-ng %{buildroot}%{_bindir}/kiwi-ng-3
mv %{buildroot}%{_bindir}/kiwicompat %{buildroot}%{_bindir}/kiwicompat-3

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

%files -n python3-%{name}
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}*
%{python3_sitelib}/%{name}*/

%files tools
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*

%files cli
%defattr(-,root,root)
%{_bindir}/%{name}*
%{_datadir}/bash-completion/completions/%{name}-ng.sh
%config(noreplace) %{_sysconfdir}/kiwi.yml

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
* 20201218195849780565 patch-tracking 9.21.5-3
- append patch file of upstream repository from <86f06b92e6d227844965d9f18e84c7da53a42b30> to <86f06b92e6d227844965d9f18e84c7da53a42b30>

* Thu Nov 26 2020 wuchaochao <wuchaochao4@huawei.com> - 9.21.5-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix issues: 124E39 125NZG

* Tue Jul 28 2020 xinghe <xinghe1@huawei.com> - 9.21.5-1
- update version to 9.21.5

* Sat Jun 20 2020 jixinjie <jixinjie@huawei.com> - 9.20.12-1
- upgrade kiwi

* Mon May 25 2020 openEuler Buildteam <buildteam@openeuler.org> - 9.19.15-3
- Rebuild for kiwi

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 9.19.15-2
- Delete redundant info in spec

* Wed Mar 18 2020 zhuchunyi <zhuchunyi@huawei.com> - 9.19.15-1
- upgrade kiwi

* Thu Feb 27 2020 lijin Yang <yanglijin@huawei.com> - 9.16.12-3
- Remove python2 dependency

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 9.16.12-2
- Package init