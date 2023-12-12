### A port of linux-cachyos-bore (https://github.com/CachyOS/linux-cachyos/tree/master/linux-cachyos-bore) for the Fedora operating system.
# https://github.com/CachyOS/linux-cachyos
### The authors of linux-cachyos patchset:
# Peter Jung ptr1337 <admin@ptr1337.dev>
# Piotr Gorski sirlucjan <piotrgorski@cachyos.org>
### The author of BORE Scheduler:
# Masahito Suzuki <firelzrd@gmail.com>
### The port maintainer for Fedora:
# bieszczaders <zbyszek@linux.pl>
# https://copr.fedorainfracloud.org/coprs/bieszczaders/

%define _build_id_links none
%define _disable_source_fetch 0

# See https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck to why this has to be done
%if 0%{?fedora} >= 37
%undefine _auto_set_build_flags
%endif

%ifarch x86_64
%define karch x86
%define asmarch x86
%endif

# whether to use LLVM-built kernel package dependencies
# The flag is not working as it should - if you want the LTO kernels to re-visit the repository, send a proper pull request.
#%define llvm_kbuild 0

%define flavor cachyos-lts
Name: kernel%{?flavor:-%{flavor}}
Summary: The Linux Kernel with Cachyos Patches

%define _basekver 6.1
%define _stablekver 66
Version: %{_basekver}.%{_stablekver}

%define customver 1
%define flaver clts%{customver}

Release:%{flaver}.0%{?dist}

%define rpmver %{version}-%{release}
%define krelstr %{release}.%{_arch}
%define kverstr %{version}-%{krelstr}

License: GPLv2 and Redistributable, no modifications permitted
Group: System Environment/Kernel
Vendor: The Linux Community and CachyOS maintainer(s)
URL: https://cachyos.org
Source0: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_basekver}.%{_stablekver}.tar.xz
Source1: https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos-lts/config
#Source0: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_basekver}.tar.xz
Patch0: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/all/0001-cachyos-base-all.patch
#Patch0: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/all/0001-cachyos-base-all-dev.patch
#Patch1: https://raw.githubusercontent.com/sirlucjan/copr-linux-cachyos/master/sources/patches/LTS/0001-zstd-%{_basekver}-merge-v1.5.5-into-kernel-tree.patch
Patch2: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/0001-Add-latency-priority-for-CFS-class.patch
#Patch2: https://raw.githubusercontent.com/sirlucjan/copr-linux-cachyos/master/sources/patches/LTS/0001-Add-latency-priority-for-CFS-class.patch
#Patch3: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched/0001-bore-cachy.patch
Patch3: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched-dev/0001-bore-cachy.patch
#Patch3: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched/0001-bore.patch
#Patch3: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched-dev/0001-bore.patch
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}
BuildRequires: 	python3-devel
BuildRequires: 	make
BuildRequires: 	findutils
BuildRequires: 	git-core
BuildRequires: 	gawk
BuildRequires: 	binutils
BuildRequires: 	m4
BuildRequires: 	tar
BuildRequires: 	hostname
BuildRequires: 	bzip2
BuildRequires: 	gzip
BuildRequires: 	xz
BuildRequires: 	diffutils
BuildRequires: 	net-tools
BuildRequires: 	elfutils
BuildRequires: 	patch
BuildRequires: 	rpm-build
BuildRequires: 	dwarves
BuildRequires: 	kmod
BuildRequires: 	libkcapi1
BuildRequires: 	perl-Carp-Always
BuildRequires: 	perl-Carp-Assert
BuildRequires: 	perl-Carp-Assert-More
BuildRequires: 	perl-Carp-Clan
BuildRequires: 	rsync
BuildRequires: 	wget 
BuildRequires: 	gcc
BuildRequires:  bash-sh
BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gcc-devel
BuildRequires:  hmaccalc
BuildRequires:  libopenssl-devel
BuildRequires:  modutils
BuildRequires:  python3-base
BuildRequires:  openssl
BuildRequires:  pesign-obs-integration
BuildRequires:  dwarves >= 1.22
BuildRequires:  libelf-devel
BuildRequires:  elfutils
BuildRequires:  zstd
%if %{llvm_kbuild}
BuildRequires: 	llvm
BuildRequires: 	clang
BuildRequires: 	lld
%endif
Requires: %{name}-core-%{rpmver} = %{kverstr}
Requires: %{name}-modules-%{rpmver} = %{kverstr}
Provides: %{name}%{_basekver} = %{rpmver}

%description
The kernel-%{flaver} meta package

%package core
Summary: Kernel core package
Group: System Environment/Kernel
Provides: installonlypkg(kernel)
Provides: kernel = %{rpmver}
Provides: kernel-core = %{rpmver}
Provides: kernel-core-uname-r = %{kverstr}
Provides: kernel-uname-r = %{kverstr}
Provides: kernel-%{_arch} = %{rpmver}
Provides: kernel-core%{_isa} = %{rpmver}
Provides: kernel-core-%{rpmver} = %{kverstr}
Provides: %{name}-core-%{rpmver} = %{kverstr}
Provides:  kernel-drm-nouveau = 16
# multiver
Provides: %{name}%{_basekver}-core = %{rpmver}
Requires: bash
Requires: coreutils
Requires: dracut
Requires: linux-firmware
Requires: /usr/bin/kernel-install
Requires: kernel-modules-%{rpmver} = %{kverstr}
Supplements: %{name} = %{rpmver}
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

%package modules
Summary: Kernel modules to match the core kernel
Group: System Environment/Kernel
Provides: installonlypkg(kernel-module)
Provides: %{name}%{_basekver}-modules = %{rpmver}
Provides: kernel-modules = %{rpmver}
Provides: kernel-modules%{_isa} = %{rpmver}
Provides: kernel-modules-uname-r = %{kverstr}
Provides: kernel-modules-%{_arch} = %{rpmver}
Provides: kernel-modules-%{rpmver} = %{kverstr}
Provides: %{name}-modules-%{rpmver} = %{kverstr}
Supplements: %{name} = %{rpmver}
%description modules
This package provides kernel modules for the core %{?flavor:%{flavor}} kernel package.

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Provides: kernel-headers = %{kverstr}
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers%{_isa} = %{kverstr}
Obsoletes: kernel-headers < %{kverstr}
Obsoletes: glibc-kernheaders < 3.0-46
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package devel
Summary: Development package for building kernel modules to match the %{?flavor:%{flavor}} kernel
Group: System Environment/Kernel
AutoReqProv: no
Requires: findutils      
Requires: perl-interpreter
Requires: openssl-devel
Requires: flex
Requires: make
Requires: bison
Requires: elfutils-libelf-devel
Requires: gcc
%if %{llvm_kbuild}
Requires: clang
Requires: llvm
Requires: lld
%endif
Enhances: akmods
Enhances: dkms
Provides: installonlypkg(kernel)
Provides: kernel-devel = %{rpmver}
Provides: kernel-devel-uname-r = %{kverstr}
Provides: kernel-devel-%{_arch} = %{rpmver}
Provides: kernel-devel%{_isa} = %{rpmver}
Provides: kernel-devel-%{rpmver} = %{kverstr}
Provides: %{name}-devel-%{rpmver} = %{kverstr}
Provides: %{name}%{_basekver}-devel = %{rpmver}
%description devel
This package provides kernel headers and makefiles sufficient to build modules
against the %{?flavor:%{flavor}} kernel package.

%package devel-matched
Summary: Meta package to install matching core and devel packages for a given %{?flavor:%{flavor}} kernel
Requires: %{name}-devel = %{rpmver},
Requires: %{name}-core = %{rpmver}
Provides: kernel-devel-matched = %{rpmver}
Provides: kernel-devel-matched%{_isa} = %{rpmver}
%description devel-matched
This meta package is used to install matching core and devel packages for a given %{?flavor:%{flavor}} kernel.

%prep
%setup -q -n linux-%{_basekver}.%{_stablekver}
#%setup -q -n linux-%{_basekver}

# Apply CachyOS patch
patch -p1 -i %{PATCH0}

# Apply ZSTD patch
#patch -p1 -i %{PATCH1}

# Apply BORE (main and sysctl) patches
patch -p1 -i %{PATCH2}
patch -p1 -i %{PATCH3}

# Fetch the config and move it to the proper directory
cp %{SOURCE1} .config

# Remove CachyOS's localversion
find . -name "localversion*" -delete
scripts/config -u LOCALVERSION

# Enable CachyOS tweaks
scripts/config -e CACHY

# Enable BORE Scheduler
scripts/config -e SCHED_BORE

# Setting tick rate
scripts/config -d HZ_300
scripts/config -e HZ_500
scripts/config --set-val HZ 500

# Disable DEBUG
scripts/config -d DEBUG_INFO
scripts/config -d DEBUG_INFO_BTF
scripts/config -d DEBUG_INFO_DWARF4
scripts/config -d DEBUG_INFO_DWARF5
scripts/config -d PAHOLE_HAS_SPLIT_BTF
scripts/config -d DEBUG_INFO_BTF_MODULES
scripts/config -d SLUB_DEBUG
scripts/config -d PM_DEBUG
scripts/config -d PM_ADVANCED_DEBUG
scripts/config -d PM_SLEEP_DEBUG
scripts/config -d ACPI_DEBUG
scripts/config -d SCHED_DEBUG
scripts/config -d LATENCYTOP
scripts/config -d DEBUG_PREEMPT

# Enable x86_64_v3
# Just to be sure, check:
# /lib/ld-linux-x86-64.so.2 --help | grep supported
# and make sure if your processor supports it:
# x86-64-v3 (supported, searched)
scripts/config -d GENERIC_CPU
scripts/config -e GENERIC_CPU3

# Set O3
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE
scripts/config -e CC_OPTIMIZE_FOR_PERFORMANCE_O3

# Enable full ticks
scripts/config -d HZ_PERIODIC
scripts/config -d NO_HZ_IDLE
scripts/config -d CONTEXT_TRACKING_FORCE
scripts/config -e NO_HZ_FULL_NODEF
scripts/config -e NO_HZ_FULL
scripts/config -e NO_HZ
scripts/config -e NO_HZ_COMMON
scripts/config -e CONTEXT_TRACKING

# Enable full preempt
scripts/config -e PREEMPT_BUILD
scripts/config -d PREEMPT_NONE
scripts/config -d PREEMPT_VOLUNTARY
scripts/config -e PREEMPT
scripts/config -e PREEMPT_COUNT
scripts/config -e PREEMPTION
scripts/config -e PREEMPT_DYNAMIC

# Unset hostname
scripts/config -u DEFAULT_HOSTNAME

# Enable SELinux (https://github.com/sirlucjan/copr-linux-cachyos/pull/1)
scripts/config --set-str CONFIG_LSM “lockdown,yama,integrity,selinux,bpf,landlock”

# Set kernel version string as build salt
scripts/config --set-str BUILD_SALT "%{kverstr}"

# Finalize the patched config
#make %{?_smp_mflags} EXTRAVERSION=-%{krelstr} oldconfig
make %{?_smp_mflags} EXTRAVERSION=-%{krelstr} olddefconfig

# Save configuration for later reuse
cat .config > config-linux-bore

%build
make %{?_smp_mflags} EXTRAVERSION=-%{krelstr}
gcc ./scripts/sign-file.c -o ./scripts/sign-file -lssl -lcrypto

%install

ImageName=$(make image_name | tail -n 1)

mkdir -p %{buildroot}/boot

cp -v $ImageName %{buildroot}/boot/vmlinuz-%{kverstr}
chmod 755 %{buildroot}/boot/vmlinuz-%{kverstr}

ZSTD_CLEVEL=19 make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install mod-fw=
make %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

# prepare -devel files
### all of the things here are derived from the Fedora kernel.spec
### see
##### https://src.fedoraproject.org/rpms/kernel/blob/rawhide/f/kernel.spec
rm -f %{buildroot}/usr/lib/modules/%{kverstr}/build
rm -f %{buildroot}/usr/lib/modules/%{kverstr}/source
mkdir -p %{buildroot}/usr/lib/modules/%{kverstr}/build
(cd %{buildroot}/usr/lib/modules/%{kverstr} ; ln -s build source)
# dirs for additional modules per module-init-tools, kbuild/modules.txt
mkdir -p %{buildroot}/usr/lib/modules/%{kverstr}/updates
mkdir -p %{buildroot}/usr/lib/modules/%{kverstr}/weak-updates
# CONFIG_KERNEL_HEADER_TEST generates some extra files in the process of
# testing so just delete
find . -name *.h.s -delete
# first copy everything
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` %{buildroot}/usr/lib/modules/%{kverstr}/build
if [ ! -e Module.symvers ]; then
touch Module.symvers
fi
cp Module.symvers %{buildroot}/usr/lib/modules/%{kverstr}/build
cp System.map %{buildroot}/usr/lib/modules/%{kverstr}/build
if [ -s Module.markers ]; then
cp Module.markers %{buildroot}/usr/lib/modules/%{kverstr}/build
fi

# create the kABI metadata for use in packaging
# NOTENOTE: the name symvers is used by the rpm backend
# NOTENOTE: to discover and run the /usr/lib/rpm/fileattrs/kabi.attr
# NOTENOTE: script which dynamically adds exported kernel symbol
# NOTENOTE: checksums to the rpm metadata provides list.
# NOTENOTE: if you change the symvers name, update the backend too
echo "**** GENERATING kernel ABI metadata ****"
gzip -c9 < Module.symvers > %{buildroot}/boot/symvers-%{kverstr}.gz
cp %{buildroot}/boot/symvers-%{kverstr}.gz %{buildroot}/usr/lib/modules/%{kverstr}/symvers.gz

# then drop all but the needed Makefiles/Kconfig files
rm -rf %{buildroot}/usr/lib/modules/%{kverstr}/build/scripts
rm -rf %{buildroot}/usr/lib/modules/%{kverstr}/build/include
cp .config %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a scripts %{buildroot}/usr/lib/modules/%{kverstr}/build
rm -rf %{buildroot}/usr/lib/modules/%{kverstr}/build/scripts/tracing
rm -f %{buildroot}/usr/lib/modules/%{kverstr}/build/scripts/spdxcheck.py

%ifarch s390x
# CONFIG_EXPOLINE_EXTERN=y produces arch/s390/lib/expoline/expoline.o
# which is needed during external module build.
if [ -f arch/s390/lib/expoline/expoline.o ]; then
cp -a --parents arch/s390/lib/expoline/expoline.o %{buildroot}/usr/lib/modules/%{kverstr}/build
fi
%endif

# Files for 'make scripts' to succeed with kernel-devel.
mkdir -p %{buildroot}/usr/lib/modules/%{kverstr}/build/security/selinux/include
cp -a --parents security/selinux/include/classmap.h %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents security/selinux/include/initial_sid_to_string.h %{buildroot}/usr/lib/modules/%{kverstr}/build
mkdir -p %{buildroot}/usr/lib/modules/%{kverstr}/build/tools/include/tools
cp -a --parents tools/include/tools/be_byteshift.h %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/tools/le_byteshift.h %{buildroot}/usr/lib/modules/%{kverstr}/build

# Files for 'make prepare' to succeed with kernel-devel.
cp -a --parents tools/include/linux/compiler* %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/linux/types.h %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/build/Build.include %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/build/Build %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/build/fixdep.c %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/objtool/sync-check.sh %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/bpf/resolve_btfids %{buildroot}/usr/lib/modules/%{kverstr}/build

cp --parents security/selinux/include/policycap_names.h %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents security/selinux/include/policycap.h %{buildroot}/usr/lib/modules/%{kverstr}/build

cp -a --parents tools/include/asm-generic %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/linux %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/asm %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/asm-generic %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/linux %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/include/vdso %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/scripts/utilities.mak %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/lib/subcmd %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/lib/*.c %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/objtool/*.[ch] %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/objtool/Build %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/objtool/include/objtool/*.h %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/lib/bpf %{buildroot}/usr/lib/modules/%{kverstr}/build
cp --parents tools/lib/bpf/Build %{buildroot}/usr/lib/modules/%{kverstr}/build

if [ -f tools/objtool/objtool ]; then
  cp -a tools/objtool/objtool %{buildroot}/usr/lib/modules/%{kverstr}/build/tools/objtool/ || :
fi
if [ -f tools/objtool/fixdep ]; then
  cp -a tools/objtool/fixdep %{buildroot}/usr/lib/modules/%{kverstr}/build/tools/objtool/ || :
fi
if [ -d arch/%{karch}/scripts ]; then
  cp -a arch/%{karch}/scripts %{buildroot}/usr/lib/modules/%{kverstr}/build/arch/%{_arch} || :
fi
if [ -f arch/%{karch}/*lds ]; then
  cp -a arch/%{karch}/*lds %{buildroot}/usr/lib/modules/%{kverstr}/build/arch/%{_arch}/ || :
fi
if [ -f arch/%{asmarch}/kernel/module.lds ]; then
  cp -a --parents arch/%{asmarch}/kernel/module.lds %{buildroot}/usr/lib/modules/%{kverstr}/build/
fi
find %{buildroot}/usr/lib/modules/%{kverstr}/build/scripts \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
%ifarch ppc64le
cp -a --parents arch/powerpc/lib/crtsavres.[So] %{buildroot}/usr/lib/modules/%{kverstr}/build/
%endif
if [ -d arch/%{asmarch}/include ]; then
  cp -a --parents arch/%{asmarch}/include %{buildroot}/usr/lib/modules/%{kverstr}/build/
fi
%ifarch aarch64
# arch/arm64/include/asm/xen references arch/arm
cp -a --parents arch/arm/include/asm/xen %{buildroot}/usr/lib/modules/%{kverstr}/build/
# arch/arm64/include/asm/opcodes.h references arch/arm
cp -a --parents arch/arm/include/asm/opcodes.h %{buildroot}/usr/lib/modules/%{kverstr}/build/
%endif
# include the machine specific headers for ARM variants, if available.
%ifarch %{arm}
if [ -d arch/%{asmarch}/mach-${Variant}/include ]; then
  cp -a --parents arch/%{asmarch}/mach-${Variant}/include %{buildroot}/usr/lib/modules/%{kverstr}/build/
fi
# include a few files for 'make prepare'
cp -a --parents arch/arm/tools/gen-mach-types %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/arm/tools/mach-types %{buildroot}/usr/lib/modules/%{kverstr}/build/

%endif
cp -a include %{buildroot}/usr/lib/modules/%{kverstr}/build/include

%ifarch i686 x86_64
# files for 'make prepare' to succeed with kernel-devel
cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_32.c %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_64.c %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs.c %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_common.c %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs.h %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/purgatory.c %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/stack.S %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/setup-x86_64.S %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/entry64.S %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/string.h %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/string.c %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/ctype.h %{buildroot}/usr/lib/modules/%{kverstr}/build/

cp -a --parents scripts/syscalltbl.sh %{buildroot}/usr/lib/modules/%{kverstr}/build/
cp -a --parents scripts/syscallhdr.sh %{buildroot}/usr/lib/modules/%{kverstr}/build/

cp -a --parents tools/arch/x86/include/asm %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/include/uapi/asm %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/objtool/arch/x86/lib %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/lib/ %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/tools/gen-insn-attr-x86.awk %{buildroot}/usr/lib/modules/%{kverstr}/build
cp -a --parents tools/objtool/arch/x86/ %{buildroot}/usr/lib/modules/%{kverstr}/build

%endif
# Clean up intermediate tools files
find %{buildroot}/usr/lib/modules/%{kverstr}/build/tools \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +

# Make sure the Makefile, version.h, and auto.conf have a matching
# timestamp so that external modules can be built
touch -r %{buildroot}/usr/lib/modules/%{kverstr}/build/Makefile \
%{buildroot}/usr/lib/modules/%{kverstr}/build/include/generated/uapi/linux/version.h \
%{buildroot}/usr/lib/modules/%{kverstr}/build/include/config/auto.conf

find %{buildroot}/usr/lib/modules/%{kverstr} -name "*.ko" -type f >modnames

# mark modules executable so that strip-to-file can strip them
xargs --no-run-if-empty chmod u+x < modnames

# Generate a list of modules for block and networking.

grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

collect_modules_list()
{
  sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
LC_ALL=C sort -u > %{buildroot}/usr/lib/modules/%{kverstr}/modules.$1
  if [ ! -z "$3" ]; then
sed -r -e "/^($3)\$/d" -i %{buildroot}/usr/lib/modules/%{kverstr}/modules.$1
  fi
}

collect_modules_list networking \
  'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
collect_modules_list block \
  'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
collect_modules_list drm \
  'drm_open|drm_init'
collect_modules_list modesetting \
  'drm_crtc_init'

# detect missing or incorrect license tags
( find %{buildroot}/usr/lib/modules/%{kverstr} -name '*.ko' | xargs /sbin/modinfo -l | \
grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

remove_depmod_files()
{
# remove files that will be auto generated by depmod at rpm -i time
pushd %{buildroot}/usr/lib/modules/%{kverstr}/
rm -f modules.{alias,alias.bin,builtin.alias.bin,builtin.bin} \
  modules.{dep,dep.bin,devname,softdep,symbols,symbols.bin}
popd
}

remove_depmod_files

mkdir -p %{buildroot}%{_prefix}/src/kernels
mv %{buildroot}/usr/lib/modules/%{kverstr}/build %{buildroot}%{_prefix}/src/kernels/%{kverstr}

# This is going to create a broken link during the build, but we don't use
# it after this point.  We need the link to actually point to something
# when kernel-devel is installed, and a relative link doesn't work across
# the F17 UsrMove feature.
ln -sf %{_prefix}/src/kernels/%{kverstr} %{buildroot}/usr/lib/modules/%{kverstr}/build

find %{buildroot}%{_prefix}/src/kernels -name ".*.cmd" -delete
#

cp -v System.map %{buildroot}/boot/System.map-%{kverstr}
cp -v System.map %{buildroot}/usr/lib/modules/%{kverstr}/System.map
cp -v .config %{buildroot}/boot/config-%{kverstr}
cp -v .config %{buildroot}/usr/lib/modules/%{kverstr}/config

(cd "%{buildroot}/boot/" && sha512hmac "vmlinuz-%{kverstr}" > ".vmlinuz-%{kverstr}.hmac")

cp -v  %{buildroot}/boot/vmlinuz-%{kverstr} %{buildroot}/usr/lib/modules/%{kverstr}/vmlinuz
(cd "%{buildroot}/usr/lib/modules/%{kverstr}" && sha512hmac vmlinuz > .vmlinuz.hmac)

# create dummy initramfs image to inflate the disk space requirement for the initramfs. 48M seems to be the right size nowadays with more and more hardware requiring initramfs-located firmware to work properly (for reference, Fedora has it set to 20M)
dd if=/dev/zero of=%{buildroot}/boot/initramfs-%{kverstr}.img bs=1M count=48

%clean
rm -rf %{buildroot}

%post core
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&
   [ -f /etc/sysconfig/kernel ]; then
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-smp$/DEFAULTKERNEL=kernel/' /etc/sysconfig/kernel || exit $?
fi
if [ -x /bin/kernel-install ] && [ -d /boot ]; then
/bin/kernel-install add %{kverstr} /usr/lib/modules/%{kverstr}/vmlinuz || exit $?
fi

%posttrans core
if [ ! -z $(rpm -qa | grep grubby) ]; then
  grubby --set-default="/boot/vmlinuz-%{kverstr}"
fi

%preun core
/bin/kernel-install remove %{kverstr} /usr/lib/modules/%{kverstr}/vmlinuz || exit $?
if [ -x /usr/sbin/weak-modules ]
then
/usr/sbin/weak-modules --remove-kernel %{kverstr} || exit $?
fi

%post devel
if [ -f /etc/sysconfig/kernel ]
then
. /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/bin/hardlink -a ! -e /run/ostree-booted ]
then
(cd /usr/src/kernels/%{kverstr} &&
 /usr/bin/find . -type f | while read f; do
   hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f 2>&1 >/dev/null
 done)
fi

%post modules
/sbin/depmod -a %{kverstr}

%postun modules
/sbin/depmod -a %{kverstr}

%files core
%ghost %attr(0600, root, root) /boot/vmlinuz-%{kverstr}
%ghost %attr(0600, root, root) /boot/System.map-%{kverstr}
%ghost %attr(0600, root, root) /boot/initramfs-%{kverstr}.img
%ghost %attr(0600, root, root) /boot/symvers-%{kverstr}.gz
%ghost %attr(0644, root, root) /boot/config-%{kverstr}
/boot/.vmlinuz-%{kverstr}.hmac
%dir /usr/lib/modules/%{kverstr}/
%dir /usr/lib/modules/%{kverstr}/kernel/
/usr/lib/modules/%{kverstr}/.vmlinuz.hmac
/usr/lib/modules/%{kverstr}/config
/usr/lib/modules/%{kverstr}/vmlinuz
/usr/lib/modules/%{kverstr}/System.map
/usr/lib/modules/%{kverstr}/symvers.gz

%files modules
%defattr (-, root, root)
/usr/lib/modules/%{kverstr}/*
%exclude /usr/lib/modules/%{kverstr}/.vmlinuz.hmac
%exclude /usr/lib/modules/%{kverstr}/config
%exclude /usr/lib/modules/%{kverstr}/vmlinuz
%exclude /usr/lib/modules/%{kverstr}/System.map
%exclude /usr/lib/modules/%{kverstr}/symvers.gz
%exclude /usr/lib/modules/%{kverstr}/build
%exclude /usr/lib/modules/%{kverstr}/source

%files headers
%defattr (-, root, root)
/usr/include/*

%files devel
%defattr (-, root, root)
/usr/src/kernels/%{kverstr}
/usr/lib/modules/%{kverstr}/build
/usr/lib/modules/%{kverstr}/source

%files devel-matched

%files
