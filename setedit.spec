Summary:	User friendly text editor
Summary(pl):	Przyjazny edytor tekstu
Name:		setedit
Version:	0.4.54
Release:	1
License:	GPL
Group:		Applications/Editors
Source0:	http://prdownloads.sourceforge.net/setedit/%{name}-%{version}.tar.gz
BuildRequires:	gcc-c++
BuildRequires:	gpm-devel
BuildRequires:	ncurses-devel
BuildRequires:	perl
BuildRequires:	gettext-devel
BuildRequires:	bzip2-devel
BuildRequires:	pcre-devel
BuildRequires:	recode
BuildRequires:	zlib-devel
BuildRequires:	librhtv-devel
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
%setup -q -n setedit

%build
rm -f Makefile
perl ./config.pl --prefix=%{_prefix} \
	--cflags="-pipe" --cxxflags="-pipe" \
	--Xcflags="%{rpmcflags}" \
	--Xcppflags="%{rpmcflags} -fno-exceptions" \
	--no-comp-exe

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix}

cp -f ./makes/linux/%{name}-%{version}/share/doc/setedit/faq.txt .

gzip -9nf README TODO faq.txt

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/*
%{_datadir}/infview
%{_datadir}/setedit
