Name:		xlockmore
Summary:	An X terminal locking program
Version:	5.43
Release:	3
License:	BSD
Group:		Graphical desktop/Other
Url:		http://www.tux.org/~bagleyd/xlockmore.html
Source0:	http://www.tux.org/~bagleyd/xlock/%name-%version/%name-%version.tar.bz2
Source1:	xlock.pamd
Patch0:		xlockmore-5.30-soundpath.patch
Patch3:		xlockmore-5.30-include_ftgl_path.patch
Requires:	pam >= 0.59
Requires:	fortune-mod
Requires:	pam
#fhimpe: needed for chkpwd group
Requires:	setup >= 2.7.12-2
BuildRequires:	pkgconfig(gtk+-x11-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(ftgl)
BuildRequires:	pam-devel 
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	xpm-devel 
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	nas-devel

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
%patch3 -p1 -b .include_ftgl_path

%{__sed} -i -e "s,/lib,/%{_lib},g" configure

%build

autoconf

%configure2_5x \
	--without-motif \
	--with-gtk2 \
	--without-gtk \
	--enable-pam --enable-bad-pam \
	--enable-syslog \
	--disable-setuid \
	--with-crypt \
	--without-rplay \
	--enable-appdefaultdir=%{_datadir}/X11/app-defaults
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/sounds/xlockmore
mkdir -p %{buildroot}%{_datadir}/xlock

install -m 755 xlock/xlock -D %{buildroot}%{_bindir}/xlock
install -m 755 xglock/xglock -D %{buildroot}%{_bindir}/xglock
install -m644 xlock/xlock.man -D %{buildroot}%{_mandir}/man1/xlock.1
install -m644 xlock/XLock.ad -D %{buildroot}%{_datadir}/X11/app-defaults/XLock
install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/pam.d/xlock
install -m755 xlock/xlock -D %{buildroot}%_bindir/xlock

cp sounds/*.au %{buildroot}%{_datadir}/sounds/xlockmore
rm -rf %{buildroot}%{_mandir}/xlock.1*


%{__mkdir_p} %{buildroot}%{_datadir}/applications

cat >> %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xlock
Comment=X11 screen saver
Icon=gnome-lockscreen
Exec=xlock
Terminal=false
Type=Application
Categories=System;
EOF

%files
%defattr(-,root,root)
%attr(4755,root,chkpwd) %{_bindir}/xlock
%{_mandir}/man1/xlock.1*
%config(noreplace) %{_datadir}/X11/app-defaults/XLock
%{_datadir}/sounds/xlockmore
%{_datadir}/applications/%{name}.desktop
%config(noreplace) %{_sysconfdir}/pam.d/*

%files gtk2
%defattr(-,root,root)
%{_bindir}/xglock
%{_datadir}/xlock
