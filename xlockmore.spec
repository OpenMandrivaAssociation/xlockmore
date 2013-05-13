Name:		xlockmore
Summary:	An X terminal locking program
Version:	5.34
Release:	%mkrel 3
License:	BSD
Group:		Graphical desktop/Other
Url:		http://www.tux.org/~bagleyd/xlockmore.html
Source:		http://www.tux.org/~bagleyd/xlock/%name-%version/%name-%version.tar.bz2
Source1:	xlock.pamd
Patch0:		xlockmore-5.30-soundpath.patch
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
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	xpm-devel 
BuildRequires:	pkgconfig(xt)
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
%patch3 -p1 -b .include_ftgl_path

%{__sed} -i -e "s,/lib,/%{_lib},g" configure

%build

export CXXFLAGS="-laudiofile"

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


%changelog
* Tue Oct 04 2011 Oden Eriksson <oeriksson@mandriva.com> 5.34-2mdv2012.0
+ Revision: 702935
- attempt to relink against libpng15.so.15

* Tue Aug 16 2011 Sergey Zhemoitel <serg@mandriva.org> 5.34-1
+ Revision: 694711
- new version 5.34

* Sun Jun 19 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 5.30-1
+ Revision: 686027
- update to new version 5.30
- rediff patch 0 and 3

* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 5.28-4
+ Revision: 671335
- mass rebuild

* Thu Jul 22 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 5.28-3mdv2011.0
+ Revision: 556942
- Replace X11-devel BR to save time

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 5.28-2mdv2010.1
+ Revision: 524451
- rebuilt for 2010.1

* Wed Aug 19 2009 Funda Wang <fwang@mandriva.org> 5.28-1mdv2010.0
+ Revision: 418045
- New version 5.28

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 5.26.1-4mdv2009.1
+ Revision: 350994
- rebuild

* Mon Aug 25 2008 Vincent Danen <vdanen@mandriva.com> 5.26.1-3mdv2009.0
+ Revision: 275957
- disable the drop_setgid patch for now

* Mon Aug 25 2008 Vincent Danen <vdanen@mandriva.com> 5.26.1-2mdv2009.0
+ Revision: 275954
- make xlock readable, maybe it will help with the inexplicable problems some are seeing with authentication issues

* Mon Aug 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.26.1-1mdv2009.0
+ Revision: 270627
- update to new version 5.26.1

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 5.25-6mdv2009.0
+ Revision: 266095
- rebuild early 2009.0 package (before pixel changes)

* Mon Jun 02 2008 Frederik Himpe <fhimpe@mandriva.org> 5.25-5mdv2009.0
+ Revision: 214356
- Add Requires: setup >= 2.7.12-2, to make sure the chkpwd group exists when installing xlockmore

* Fri May 23 2008 Vincent Danen <vdanen@mandriva.com> 5.25-4mdv2009.0
+ Revision: 210183
- make it sgid chkpwd

* Thu May 22 2008 Vincent Danen <vdanen@mandriva.com> 5.25-3mdv2009.0
+ Revision: 210090
- add a patch to drop sgid calls and make xlock sgid shadow so that it will work again with both shadow and tcb passwording

* Fri May 16 2008 Paulo Andrade <pcpa@mandriva.com.br> 5.25-2mdv2009.0
+ Revision: 208015
- Fix remaining of an alternative correction, that would require adding
  librplay to the distro being commited.
- By default, don't build with rplay, if it is available in the
  "Build System". This should be only an issue for people building
  rpms from source. And should address #38171
  ("xlockmore for build needs librplay-devel if librplay installed")

* Sat Feb 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.25-1mdv2008.1
+ Revision: 174085
- new license policy
- drop patch 0
- add desktop entry for xflock
- enable syslog logging
- spec file clean
- new version 5.25

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jun 21 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 5.23-1mdv2008.0
+ Revision: 42343
- New upstream release: 5.23


* Tue Mar 06 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 5.22-5mdv2007.0
+ Revision: 133664
- fix the path to look for app-defaults (#23242)
- fix the path to look for sounds (#17792)

* Sat Feb 10 2007 Michael Scherer <misc@mandriva.org> 5.22-4mdv2007.1
+ Revision: 118678
- do not use pam_stack
- bunzip patchs

* Fri Dec 22 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 5.22-3mdv2007.1
+ Revision: 101842
- fix build

* Thu Aug 31 2006 Antonio Hobmeir Neto <neto@mandriva.com> 5.22-2mdv2007.0
+ Revision: 58917
- Add a symlink to /usr/lib/X11/app-default/XLock (#23242)
- Add missing build requires for gtk+2-devel

  + Gustavo Pichorim Boiko <boiko@mandriva.com>
    - Import xlockmore

* Wed Jun 28 2006 Eskild Hustvedt <eskild@mandriva.org> 5.22-1mdv
- New version 5.22
- Dropped patch2 - merged upstream
- Rediffed patch1
- Now compiles the gtk2 front-end, found in the -gtk2 subpackage

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 5.19-3mdk
- Rebuild

* Wed Aug 17 2005 Samir Bellabes <sbellabes@mandriva.com> 5.19-2mdk
- Use workaround for pam problem (same as for Gentoo) (bug #17504)
- fix bad path for including FTGL's header
- And it should be a good idea to test package before uploading, next time

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 5.19-1mdk
- new release

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 5.18-1mdk
- new release from Crispin Boylan
- %%mkrel

* Thu Jun 10 2004 Götz Waschk <waschk@linux-mandrake.com> 5.11-2mdk
- rebuild for new g++

