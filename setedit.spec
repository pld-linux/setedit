Summary:	User friendly text editor
Summary(pl):	Przyjazny edytor tekstu
Name:		setedit
Version:	0.5.2
Release:	1
License:	GPL
Group:		Applications/Editors
Source0:	http://dl.sourceforge.net/setedit/%{name}-%{version}.tar.gz
# Source0-md5:	86e4d5f345f9667c1d77a805d6a29173
Patch0:		%{name}-gettext.patch
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
%patch -p1

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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README TODO distrib/linux.faq
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/setedit
%attr(755,root,root) %{_libdir}/setedit/*.so
%{_libdir}/setedit/holidays.conf
%{_datadir}/infview
%{_datadir}/setedit
%{_infodir}/*.info*
%{_mandir}/man1/*
