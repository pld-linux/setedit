# TODO:
# - build and use shared library libset
Summary:	User friendly text editor
Summary(pl):	Przyjazny edytor tekstu
Name:		setedit
Version:	0.5.4
Release:	1
License:	GPL
Group:		Applications/Editors
Source0:	http://dl.sourceforge.net/setedit/%{name}-%{version}.tar.gz
# Source0-md5:	fc2f9724f11965fbd11475ff9235eaa0
#Patch0:                %{name}-fixlib.patch
URL:		http://setedit.sourceforge.net/
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
player, etc).

%description -l pl
Setedit to bardzo przyjazny edytor tekstu (z okienkami, menu, itd.).
Ma on kilka "wodotrysków" np. odtwarzacz plików MP3. W zestawie jest
tak¿e program infview do wy¶wietlania plików .info.

%package -n infview
Summary:	Viewer of info pages
Summary(pl):	Przegl±darka plików .info
Group:		Applications/Text

%description -n infview
Viewer of .info pages.

%description -n infview -l pl
Przegl±darka plików .info.

%package devel
Summary:	Development files for setedit
Summary(pl):	Pliki biblioteczne setedit
Group:		Development/Libraries

%description devel
Development files for setedit.

%description devel -l pl
Pliki biblioteczne setedit.

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
%{__make} -C makes libset

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix}

# install library by hand
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/%{name}}
cp makes/lib*.a $RPM_BUILD_ROOT%{_libdir}
# remove non-object files from archives - they brak stripping
for i in $RPM_BUILD_ROOT%{_libdir}/*.a; do
	ar d $i rhide.env common.imk
done
ar d $RPM_BUILD_ROOT%{_libdir}/libset.a libeasyd.a libsettv.a

cp -r include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}
for dir in infview sdg setedit settvuti; do
	install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/$dir
	cp -r $dir/include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/$dir
done

rm -rf doc-setedit doc-infview
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

%files -n infview
%defattr(644,root,root,755)
%doc doc-infview/*
%attr(755,root,root) %{_bindir}/infview
%{_datadir}/infview
%{_infodir}/infview.info*
%{_mandir}/man1/infview*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_libdir}/lib*.a
