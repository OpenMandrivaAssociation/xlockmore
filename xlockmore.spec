%define	name	xlockmore
%define	version	5.22
%define release	%mkrel 5
%define	enable_matrix	0

# Allow --with[out] <feature> at rpm command line build
%{?_without_matrix: %{expand: %%define enable_matrix 0}}
%{?_with_matrix: %{expand: %%define enable_matrix 1}}


Name: 		%{name}
Summary:	An X terminal locking program
Version: 5.23
Release: %mkrel 1
License:	MIT
Group:		Graphical desktop/Other
Url:		http://www.tux.org/~bagleyd/xlockmore.html
Source:		ftp://ftp.tux.org/pub/tux/bagleyd/xlockmore/%{name}-%{version}.tar.bz2
Source1:	xlock.pamd
Patch0:		xlockmore-5.22-soundpath.patch
# Disable the matrix screensaver
Patch1:		xlockmore-5.22-matrix.patch
Patch3:		xlockmore-5.19-include_ftgl_path.patch
Requires:	pam >= 0.59 
Requires:	fortune-mod
Requires:	%{_sysconfdir}/pam.d/system-auth
BuildRequires: esound-devel 
BuildRequires: gtk+2-devel
BuildRequires: mesa-common-devel 
BuildRequires: pam-devel 
BuildRequires: X11-devel 
BuildRequires: xpm-devel 

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it.  Xlockmore runs a provided screensaver until you type
in your password.

Install the xlockmore package if you need a locking program to secure
X sessions.

%package gtk2
Summary:	A GTK2 front-end to xlockmore
Url:            http://www.tux.org/~bagleyd/xlockmore.html
Group:          Graphical desktop/Other
License:	MIT
Requires:	xlockmore

%description gtk2
A GTK2 front-end to xlockmore

%prep
%setup -q
%patch0 -p1 -b .soundpath
%if !%enable_matrix
%patch1 -p0 -b .matrix
%endif
%patch3 -p1 -b .include_ftgl_path

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS" %configure2_5x 	--without-motif \
					--with-gtk2 \
					--without-gtk \
					--enable-pam \
					--enable-appdefaultdir=%{_sysconfdir}/X11/app-defaults
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sounds/xlockmore

perl -p -i -e 's/-o root//g' Makefile */Makefile
%makeinstall

install -m644 xlock/xlock.man -D $RPM_BUILD_ROOT%{_mandir}/man1/xlock.1
install -m644 xlock/XLock.ad -D $RPM_BUILD_ROOT%{_sysconfdir}/X11/app-defaults/XLock
install -m644 %SOURCE1 -D $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/xlock

cp sounds/*.au $RPM_BUILD_ROOT%{_datadir}/sounds/xlockmore
rm -rf $RPM_BUILD_ROOT%{_mandir}/xlock.1*
chmod 755 $RPM_BUILD_ROOT%{_bindir}/xlock

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/xlock
%{_mandir}/man1/xlock.1*
%config(noreplace) %{_sysconfdir}/X11/app-defaults/XLock
%{_datadir}/sounds/xlockmore
%config(noreplace) %{_sysconfdir}/pam.d/*

%files gtk2
%defattr(-,root,root)
%{_bindir}/xglock
%{_datadir}/xlock


