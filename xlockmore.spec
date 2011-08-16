Name:		xlockmore
Summary:	An X terminal locking program
Version:	5.34
Release:	%mkrel 1
License:	BSD
Group:		Graphical desktop/Other
Url:		http://www.tux.org/~bagleyd/xlockmore.html
Source:		http://www.tux.org/~bagleyd/xlock/%name-%version/%name-%version.tar.bz2
Source1:	xlock.pamd
Patch0:		xlockmore-5.30-soundpath.patch
Patch1:		xlockmore-5.25-drop_setgid.patch
Patch3:		xlockmore-5.30-include_ftgl_path.patch
Requires:	pam >= 0.59
Requires:	fortune-mod
Requires:	pam
#fhimpe: needed for chkpwd group
Requires:	setup >= 2.7.12-2
BuildRequires:	esound-devel 
BuildRequires:	gtk+2-devel
BuildRequires:	mesa-common-devel 
BuildRequires:	pam-devel 
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	xpm-devel 
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The xlockmore utility is an enhanced version of the standard xlock
program, which allows you to lock an X session so that other users
can't access it.  Xlockmore runs a provided screensaver until you type
in your password.

Install the xlockmore package if you need a locking program to secure
X sessions.

%package gtk2
Summary:	A GTK2 front-end to xlockmore
Url:		http://www.tux.org/~bagleyd/xlockmore.html
Group:		Graphical desktop/Other
License:	BSD
Requires:	xlockmore

%description gtk2
A GTK2 front-end to xlockmore.

%prep
%setup -q
%patch0 -p1 -b .soundpath
#%patch1 -p0 -b .drop_setgid
%patch3 -p1 -b .include_ftgl_path

%{__sed} -i -e "s,/lib,/%{_lib},g" configure

%build
autoconf

%configure2_5x \
	--without-motif \
	--with-gtk2 \
	--without-gtk \
	--enable-pam \
	--enable-syslog \
	--disable-setuid \
	--with-crypt \
	--without-rplay \
	--enable-appdefaultdir=%{_datadir}/X11/app-defaults
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/sounds/xlockmore

perl -p -i -e 's/-o root//g' Makefile */Makefile
%makeinstall

install -m644 xlock/xlock.man -D %{buildroot}%{_mandir}/man1/xlock.1
install -m644 xlock/XLock.ad -D %{buildroot}%{_datadir}/X11/app-defaults/XLock
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/pam.d/xlock

cp sounds/*.au %{buildroot}%{_datadir}/sounds/xlockmore
rm -rf %{buildroot}%{_mandir}/xlock.1*
chmod 755 %{buildroot}%{_bindir}/xlock


%{__mkdir_p} %{buildroot}%{_datadir}/applications

cat >> %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xlock
Comment=X11 screen saver
Icon=gnome-lockscreen.png
Exec=xlock
Terminal=false
Type=Application
Category=System;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(2755,root,chkpwd) %{_bindir}/xlock
%{_mandir}/man1/xlock.1*
%config(noreplace) %{_datadir}/X11/app-defaults/XLock
%{_datadir}/sounds/xlockmore
%{_datadir}/applications/%{name}.desktop
%config(noreplace) %{_sysconfdir}/pam.d/*

%files gtk2
%defattr(-,root,root)
%{_bindir}/xglock
%{_datadir}/xlock
