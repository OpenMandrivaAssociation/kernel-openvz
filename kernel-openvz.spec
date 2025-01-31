# -*- Mode: rpm-spec -*-
#
# (c) Mandriva
#
# The kernel-2.6-linus package (and so this spec file) is under development,
# it does mean:
#
#    1. You can have nasty surprises when playing with the package
#    generation
#
#    2. Is easier to go and come back from Mordor than adding a new
#    architecture support
#
#    3. A known architecture with just a missing .config shouldn't be too
#    hard, but as this spec changes too fast, it's likely to be broken
#
#
# if you try to understand kernel numbering, read docs/kernel_naming

%define kernelversion	2
%define patchlevel	6
%define sublevel	26

# kernel Makefile extraversion is substituted by
# kpatch/kstable wich are either 0 (empty), rc (kpatch) or stable release (kstable)
%define kpatch		0
%define kstable		0

%define ktag		openvz

# checkhov's release
%define openvz_rel		1

# this is the releaseversion
%define mdvrelease 	1

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define kname 		kernel-%{ktag}

%define rpmtag		%distsuffix
%if %kpatch
%define rpmrel		%mkrel 0.%{kpatch}.%{ktag}%{openvz_rel}.%{mdvrelease}
%else
%define rpmrel		%mkrel 1.%{ktag}%{openvz_rel}.%{mdvrelease}
%endif

# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver	  	%{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%endif
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths
%if %kpatch
%define buildrpmrel     0.%{kpatch}.%{ktag}%{openvz_rel}.%{mdvrelease}%{rpmtag}
%else
%define buildrpmrel     1.%{ktag}%{openvz_rel}.%{mdvrelease}%{rpmtag}
%endif

%define buildrel        %{kversion}-%{buildrpmrel}

%define openvz_info NOTE: This kernel has no Mandriva patches and no third-party drivers, \
only openvz series patches applied to vanille kernel.org kernels.

# having different top level names for packges means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       ${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_doc 0
%define build_source 1
%define build_devel 1
%define build_debug 1

%define build_kernel 1

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)

# End of user definitions
%{?_without_kernel: %global build_kernel 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}

%{?_with_kernel: %global build_kernel 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}


%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make
%endif
# there are places where parallel make don't work
%define smake make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/" -e "s/sparc/%{_target_cpu}/" -e "s/i386/x86/" -e "s/x86_64/x86/")

# src.rpm description
Summary: 	The Linux kernel (the core of the Linux operating system)
Name:           %{kname}
Version:        %{kversion}
Release:        %{rpmrel}
License: 	GPLv2
Group: 		System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64 sparc64
ExclusiveOS: 	Linux
URL: 		https://www.kernel.org/

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign
# This is for disabling mrproper on -devel rpms
Source2:		disable-mrproper-in-devel-rpms.patch

Source4:  README.kernel-sources
Source5:  README.MandrivaLinux

Source20: i386.config
Source21: i386-pae.config
Source22: x86_64.config


####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing

%if %kpatch
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kstable
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif

# checkhov patches
%if %kpatch
Patch2:		linux-2.6.0-nonintconfig.patch
%else
Patch2:		linux-2.6.0-nonintconfig.patch
%endif

# checkhov patches
%if %kpatch
Patch100:		http://download.openvz.org/kernel/branches/2.6.26/current/patches/patch-chekhov.1-combined.gz
%else
Patch100:		http://download.openvz.org/kernel/branches/2.6.26/current/patches/patch-chekhov.1-combined.gz
%endif

# checkhov patches
%if %kpatch
Patch2100: patch-linux-2.6.26-openvz-drbd-8.2.6
%else
Patch2100: patch-linux-2.6.26-openvz-drbd-8.2.6
%endif

# checkhov patches
%if %kpatch
Patch2101: diff-drbd-proc-fix
%else
Patch2101: diff-drbd-proc-fix
%endif

# LKML's patches

# MDV Patches

#END
####################################################################

# Defines for the things that are needed for all the kernels
%define requires1 module-init-tools >= 3.0-%mkrel 7
%define requires2 mkinitrd >= 3.4.43-%mkrel 10
%define requires3 bootloader-utils >= 1.9
%define requires4 sysfsutils module-init-tools >= 0.9.15
%define requires5 kernel-firmware >= 2.6.27-0.rc2.2mdv

%define kprovides kernel = %{tar_ver}, alsa

Conflicts: drakxtools-backend < 10.4.140
BuildRoot: 	%{_tmppath}/%{name}-%{kversion}-build-%{_arch}
Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
Source package to build the Linux kernel.

%{openvz_info}


#
# kernel: Symmetric MultiProcessing kernel
#
%if %build_kernel
%package -n %{kname}-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  The Linux Kernel compiled for SMP machines
Group: 	  System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3
Requires: %requires4
Requires: %requires5

%description -n %{kname}-%{buildrel}
This package includes a SMP version of the Linux %{kversion} kernel. It is
required only on machines with two or more CPUs, although it should work
fine on single-CPU boxes.
This kernel relies on in-kernel smp alternatives to switch between
up & smp mode depending on detected hardware. To force the kernel
to boot in single processor mode, use the "nosmp" boot parameter.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{openvz_info}
%endif # build_kernel

#
# kernel-source: kernel sources
#
%if %build_source
%package -n %{kname}-source-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: %{kname}-source, kernel-source = %{kverrel}, kernel-devel = %{kverrel}
Provides: %{kname}-source-%{kernelversion}.%{patchlevel}
Requires: glibc-devel, ncurses-devel, make, gcc, perl
Summary:  The source code for the Linux kernel
Group:    Development/Kernel
Autoreqprov: no

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the Linux
kernel. Theese source files are only needed if you want to build your own
custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{openvz_info}
%endif # build_source


#
# kernel-devel: stripped kernel sources
#
%if %build_devel
%package -n %{kname}-devel-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: kernel-devel = %{kverrel}
Summary:  The %{kname} devel files for 3rdparty modules build
Group:    Development/Kernel
Autoreqprov: no
Requires: glibc-devel, ncurses-devel, make, gcc, perl

%description -n %{kname}-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build
3rdparty drivers against for use with the %{kname}-%{buildrel}.

If you want to build your own kernel, you need to install the full
%{kname}-source-%{buildrel} rpm.

%{openvz_info}
%endif # build_devel

#
# kernel-debug: unstripped kernel vmlinux
#
%if %build_debug
%package -n %{kname}-debug-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Provides: kernel-debug = %{kverrel}
Summary:  The %{kname} debug files
Group:    Development/Kernel
Autoreqprov: no
Requires: glibc-devel

%description -n %{kname}-debug-%{buildrel}
This package contains the kernel-debug files that should be enough to
use debugging/monitoring tool (like systemtap, oprofile, ...)

%{openvz_info}
%endif # build_debug

#
# kernel-doc: documentation for the Linux kernel
#
%if %build_doc
%package -n %{kname}-doc-%{buildrel}
Version:  %{fakever}
Release:  %{fakerel}
Summary:  Various documentation bits found in the kernel source
Group:    Books/Computer books

%description -n %{kname}-doc-%{buildrel}
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate

%{openvz_info}
%endif # build_doc


#
# kernel-latest: virtual rpm
#
%if %build_kernel
%package -n %{kname}-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-%{buildrel}
Obsoletes:	%{kname}-smp-latest

%description -n %{kname}-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname} installed...

%{openvz_info}
%endif # build_kernel


#
# kernel-source-latest: virtual rpm
#
%if %build_source
%package -n %{kname}-source-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-source-%{buildrel}

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...

%{openvz_info}
%endif # build_source


#
# kernel-devel-latest: virtual rpm
#
%if %build_devel
%package -n %{kname}-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-devel-%{buildrel}
Obsoletes:	%{kname}-headers-latest
Obsoletes:	%{kname}-smp-devel-latest
Obsoletes:	%{kname}-smp-headers-latest

%description -n %{kname}-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-devel installed...

%{openvz_info}
%endif # build_devel


#
# kernel-debug-latest: virtual rpm
#
%if %build_debug
%package -n %{kname}-debug-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-debug
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-debug-%{buildrel}

%description -n %{kname}-debug-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-debug installed...

%{openvz_info}
%endif # build_debug

#
# kernel-doc-latest: virtual rpm
#
%if %build_doc
%package -n %{kname}-doc-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-doc
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-doc-%{buildrel}

%description -n %{kname}-doc-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-doc installed...

%{openvz_info}
%endif

#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

pushd %src_dir
%if %kpatch
%patch1 -p1
%endif
%if %kstable
%patch1 -p1
%endif

# openvz's patch
# %patch2 -p0

%patch100 -p1

#%patch2100 -p1
#%patch2101 -p1

# LKML's patches

# MDV Patches

popd

# PATCH END


#
# Setup Begin
#

pushd ${RPM_SOURCE_DIR}

#
# Copy our defconfigs into place.
cp -f %{_arch}.config     %{build_dir}/linux-%{tar_ver}/arch/%{target_arch}/defconfig
popd

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" linux-%{tar_ver}/Makefile


%build
# Common target directories
%define _kerneldir /usr/src/%{kname}-%{buildrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _develdir /usr/src/%{kname}-devel-%{buildrel}


# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_devel %{temp_root}%{_develdir}


PrepareKernel() {
	name=$1
	extension=$2
	echo "Prepare compilation of kernel $extension"

	if [ "$name" ]; then
		config_name="defconfig-$name"
	else
		config_name="defconfig"
	fi

	# make sure EXTRAVERSION says what we want it to say
	%if %kstable
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-$extension/" Makefile
	%else
		LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
	%endif

	### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
	LC_ALL=C perl -p -i -e "s/^source/### source/" drivers/crypto/Kconfig

	%smake -s mrproper
	cp arch/%{target_arch}/$config_name .config
	%smake oldconfig
}


BuildKernel() {
	KernelVer=$1
	echo "Building kernel $KernelVer"

	%kmake all

	## Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	%ifarch sparc64
	gzip -9c vmlinux > %{temp_boot}/vmlinuz-$KernelVer
	cp -f vmlinux %{temp_boot}/vmlinux-$KernelVer
	%else
	cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	cp -f vmlinux %{temp_boot}/vmlinux-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install
}


SaveDevel() {
	flavour=$1
	if [ "$flavour" = "up" ]; then
		DevelRoot=%{temp_devel}
	else
		DevelRoot=%{temp_smp_devel}
	fi
	mkdir -p $DevelRoot
	for i in $(find . -name 'Makefile*'); do cp -R --parents $i $DevelRoot;done
	for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i $DevelRoot;done
	cp -fR include $DevelRoot
	cp -fR scripts $DevelRoot
	%ifarch %{ix86} x86_64
		cp -fR arch/x86/kernel/asm-offsets.{c,s} $DevelRoot/arch/x86/kernel/
		cp -fR arch/x86/kernel/asm-offsets_{32,64}.c $DevelRoot/arch/x86/kernel/
	%else
		cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $DevelRoot/arch/%{target_arch}/kernel/
	%endif
	cp -fR .config Module.symvers $DevelRoot

        # Needed for truecrypt build (Danny)
	cp -fR drivers/md/dm.h $DevelRoot/drivers/md/

	# fix permissions
	chmod -R a+rX $DevelRoot
}

SaveDebug() {
	kernversion=$1
	flavour=$2

	echo "SaveDebug $kernversion $flavour"

	kernel_debug_files=../kernel_debug_files.$flavour

	echo "%defattr(-,root,root)" > $kernel_debug_files
	echo "%{_bootdir}/vmlinux-$kernversion" >> $kernel_debug_files

	find %{temp_modules}/$kernversion/kernel \
		-name "*.ko" -exec objcopy --only-keep-debug '{}' '{}'.debug \;

	find %{temp_modules}/$kernversion/kernel \
		-name "*.ko" -exec objcopy --add-gnu-debuglink='{}'.debug --strip-debug '{}' \;

	pushd %{temp_modules}
	find $kernversion/kernel -name "*.ko.debug" > debug_module_list
	popd

	cat %{temp_modules}/debug_module_list | sed 's|\(.*\)|%{_modulesdir}/\1|' >> $kernel_debug_files
	cat %{temp_modules}/debug_module_list | sed 's|\(.*\)|%exclude %{_modulesdir}/\1|' >> ../kernel_exclude_debug_files.$flavour
	rm -f %{temp_modules}/debug_module_list
}


CreateFiles() {
	kernversion=$1
	flavour=$2

	echo "CreateFiles $kernversion $flavour"

	output=../kernel_files.$kernversion

	echo "%defattr(-,root,root)" > $output
	echo "%{_bootdir}/config-${kernversion}" >> $output
	echo "%{_bootdir}/vmlinuz-${kernversion}" >> $output
	echo "%{_bootdir}/System.map-${kernversion}" >> $output
	echo "%dir %{_modulesdir}/${kernversion}/" >> $output
	echo "%{_modulesdir}/${kernversion}/kernel" >> $output
	echo "%{_modulesdir}/${kernversion}/modules.*" >> $output
	echo "%doc README.kernel-sources" >> $output
	echo "%doc README.MandrivaLinux" >> $output
	cat ../kernel_exclude_debug_files.$flavour >> $output
}


CreateKernel() {
	flavour=$1
	echo "CreateKernel $flavour"

	if [ "$flavour" = "up" ]; then
		KernelVer=%{buildrel}
		PrepareKernel "" %{buildrpmrel}
	else
		KernelVer=%{buildrel}$flavour
		PrepareKernel $flavour %{buildrpmrel}$flavour
	fi

	BuildKernel $KernelVer
	%if %build_devel
	    SaveDevel $flavour
	%endif
	%if %build_debug
	    SaveDebug $KernelVer $flavour
	%endif
        CreateFiles $KernelVer $flavour
}


###
# DO it...
###


# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}


#make sure we are in the directory
cd %src_dir

%if %build_kernel
CreateKernel up
%endif


# We don't make to repeat the depend code at the install phase
%if %build_source
PrepareKernel "" %{buildrpmrel}custom
# From > 2.6.13 prepare-all is deprecated and relies on include/linux/autoconf
# To have modpost and others scripts, one has to use the target scripts
%smake -s prepare
%smake -s scripts
%endif


###
### install
###
%install

# on ne strippe pas vmlinux
EXCLUDE_FROM_STRIP="%{_bootdir}/vmlinux"
export EXCLUDE_FROM_STRIP

install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_devel %{buildroot}%{_develdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source}

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}


# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu mn10300 parisc powerpc ppc sh sh64 s390 v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i

%if %build_devel
%if %build_kernel
	rm -rf %{target_devel}/arch/$i
	rm -rf %{target_devel}/include/asm-$i
%endif # build_kernel
# Needed for truecrypt build (Danny)
%if %build_kernel
	cp -fR drivers/md/dm.h %{target_devel}/drivers/md/
%endif # build_kernel
%endif # build_devel
done

# remove arch files based on target arch
%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/x86
	rm -rf %{target_source}/include/asm-x86
%if %build_devel
%if %build_kernel
	rm -rf %{target_devel}/arch/x86
	rm -rf %{target_devel}/include/asm-x86
%endif # build_kernel
%endif # build_devel
%endif # ifnarch %{ix86} x86_64
%ifnarch sparc sparc64
	rm -rf %{target_source}/arch/sparc
	rm -rf %{target_source}/arch/sparc64
	rm -rf %{target_source}/include/asm-sparc
	rm -rf %{target_source}/include/asm-sparc64
%if %build_devel
%if %build_kernel
	rm -rf %{target_devel}/arch/sparc
	rm -rf %{target_devel}/arch/sparc64
	rm -rf %{target_devel}/include/asm-sparc
	rm -rf %{target_devel}/include/asm-sparc64
%endif # build_kernel
%endif # build_devel
%endif # ifnarch sparc sparc64

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check,.mailmap,.missing-syscalls.d,.mm,arch/.gitignore}

# disable mrproper in -devel rpms
%if %build_devel
%if %build_kernel
patch -p1 -d %{target_devel} -i %{SOURCE2}
%endif # build_kernel
%endif # build_devel

#endif %build_source
%endif

# gzipping modules
find %{target_modules} -name "*.ko" | xargs gzip -9

# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

for i in %{target_modules}/*; do
  rm -f $i/build $i/source $i/modules.*
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here

pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | xargs /sbin/modinfo-25 \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd



###
### clean
###

%clean
rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be
# able to do several rpm --short-circuit -bi for testing install
# phase without repeating compilation phase
#rm -rf %{temp_root}



###
### scripts
###

### kernel
%preun -n %{kname}-%{buildrel}
/sbin/installkernel -R %{buildrel}
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0

%post -n %{kname}-%{buildrel}
/sbin/installkernel -L %{buildrel}
if [ -d /usr/src/%{kname}-devel-%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%postun -n %{kname}-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}


### kernel-devel
%post -n %{kname}-devel-%{buildrel}
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{buildrel} ]; then
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/build
    ln -sf /usr/src/%{kname}-devel-%{buildrel} /lib/modules/%{buildrel}/source
fi

%preun -n %{kname}-devel-%{buildrel}
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{buildrel}/build ]; then
    rm -f /lib/modules/%{buildrel}/build
fi
if [ -L /lib/modules/%{buildrel}/source ]; then
    rm -f /lib/modules/%{buildrel}/source
fi
exit 0


### kernel-source
%post -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}*; do
	if [ -d $i ]; then
	        rm -f $i/{build,source}
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/build
	        ln -sf /usr/src/%{kname}-%{buildrel} $i/source
	fi
done

%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{buildrel}/{build,source}; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0


###
### file lists
###

#
# kernel
#
%if %build_kernel
%files -n %{kname}-%{buildrel} -f kernel_files.%{buildrel}
%endif # build_kernel

#
# kernel-source
#
%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
#{_kerneldir}/Module.markers
%{_kerneldir}/arch/Kconfig
%ifarch sparc sparc64
%{_kerneldir}/arch/sparc
%{_kerneldir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/x86
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm
%{_kerneldir}/include/asm-generic
%ifarch sparc sparc64
%{_kerneldir}/include/asm-sparc
%{_kerneldir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-x86
%endif
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/config
%{_kerneldir}/include/crypto
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
#%{_kerneldir}/include/trace
%{_kerneldir}/include/bc
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/keys
%{_kerneldir}/include/rdma
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/samples
%{_kerneldir}/security
%{_kerneldir}/scripts
%{_kerneldir}/sound
%{_kerneldir}/usr
%{_kerneldir}/virt/kvm
%{_kerneldir}/COPYING.SWsoft
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif

#
# kernel-devel
#
%if %build_devel
%files -n %{kname}-devel-%{buildrel}
%defattr(-,root,root)
%dir %{_develdir}
%dir %{_develdir}/arch
%dir %{_develdir}/include
%{_develdir}/.config
%{_develdir}/Documentation
%{_develdir}/Kbuild
%{_develdir}/Makefile
%{_develdir}/Module.symvers
%{_develdir}/arch/Kconfig
%ifarch sparc sparc64
%{_develdir}/arch/sparc
%{_develdir}/arch/sparc64
%endif
%ifarch %{ix86} x86_64
%{_develdir}/arch/x86
%endif
%{_develdir}/arch/um
%{_develdir}/block
%{_develdir}/crypto
%{_develdir}/drivers
%{_develdir}/fs
%{_develdir}/include/Kbuild
%{_develdir}/include/acpi
%{_develdir}/include/asm
%{_develdir}/include/asm-generic
%ifarch sparc sparc64
%{_develdir}/include/asm-sparc
%{_develdir}/include/asm-sparc64
%endif
%ifarch %{ix86} x86_64
%{_develdir}/include/asm-x86
%endif
%{_develdir}/include/asm-um
%{_develdir}/include/config
%{_develdir}/include/crypto
%{_develdir}/include/keys
%{_develdir}/include/linux
%{_develdir}/include/math-emu
%{_develdir}/include/mtd
%{_develdir}/include/net
%{_develdir}/include/pcmcia
%{_develdir}/include/rdma
%{_develdir}/include/scsi
%{_develdir}/include/sound
#%{_develdir}/include/trace
%{_develdir}/include/bc
%{_develdir}/include/video
%{_develdir}/include/media
%{_develdir}/include/rxrpc
%{_develdir}/include/xen
%{_develdir}/init
%{_develdir}/ipc
%{_develdir}/kernel
%{_develdir}/lib
%{_develdir}/mm
%{_develdir}/net
%{_develdir}/samples
%{_develdir}/scripts
%{_develdir}/security
%{_develdir}/sound
%{_develdir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif # kernel_devel

#
# kernel-debug
#
%if %build_debug
%files -n %{kname}-debug-%{buildrel} -f kernel_debug_files.up
%endif # build_debug


#
# kernel-doc
#
%if %build_doc
%files -n %{kname}-doc-%{buildrel}
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif # kernel_doc

#
# kernel-latest
#
%if %build_kernel
%files -n %{kname}-latest
%defattr(-,root,root)
%endif # build_kernel

#
# kernel-source-latest
#
%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif

#
# kernel-devel-latest
#
%if %build_devel
%files -n %{kname}-devel-latest
%defattr(-,root,root)
%endif # build_devel

#
# kernel-debug-latest
#
%if %build_debug
%files -n %{kname}-debug-latest
%defattr(-,root,root)
%endif # build_debug

#
# kernel-doc-latest
#
%if %build_doc
%files -n %{kname}-doc-latest
%defattr(-,root,root)
%endif # build_doc
