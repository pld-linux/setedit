# TODO: 
# - infview to separate package
# - libraries and devel files (needed by rhide) to separate packages.
%define	snap	20040910
Summary:	User friendly text editor
Summary(pl):	Przyjazny edytor tekstu
Name:		setedit
Version:	0.5.4
Release:	0.%{snap}.0.1
License:	GPL
Group:		Applications/Editors
# note - it's really snap version, waiting for final release
Source0:	http://setedit.sourceforge.net/%{name}-%{version}.tar.gz
# Source0-md5:	aa6a0533a4e1ebf7fb07a5398ce0d465
BuildRequires:	aalib-devel
BuildRequires:	bzip2-devel >= 0.9.5d
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel >= 1.10
BuildRequires:	librhtv-devel >= 2.0.2
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	pcre-devel
BuildRequires:	perl-base
BuildRequires:	recode
BuildRequires:	zlib-devel >= 1.1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Setedit is text editor, which uses Turbo Vision (menus, windows like
in many DOS applications). It has some interesting features (MP3
player, etc). There is infview (viewer of info pages) in package also.

%description -l pl
Setedit to bardzo przyjazny edytor tekstu (z okienkami, menu, itd.).
Ma on kilka "wodotrysków" np. odtwarzacz plików MP3. W zestawie jest
tak¿e program infview do wy¶wietlania plików .info.

%prep
%setup -q -n %{name}

%build
rm -f Makefile
%{__perl} ./config.pl \
	--prefix=%{_prefix} \
	--cflags="-pipe" \
	--cxxflags="-pipe" \
	--Xcflags="%{rpmcflags}" \
	--Xcppflags="%{rpmcflags} -fno-exceptions" \
	--no-comp-exe \
	--fhs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix}

mv $RPM_BUILD_ROOT%{_docdir}/setedit doc-setedit
mv $RPM_BUILD_ROOT%{_docdir}/infview doc-infview

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README TODO distrib/linux.faq doc-setedit/*
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/setedit
%attr(755,root,root) %{_libdir}/setedit/*.so
%{_libdir}/setedit/holidays.conf
%{_datadir}/setedit
%{_infodir}/s*.info*
%{_mandir}/man1/setedit*
