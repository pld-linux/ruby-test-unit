#
# Conditional build:
%bcond_without	tests		# build without tests

%define pkgname test-unit
Summary:	Improved version of Test::Unit bundled in Ruby 1.8.x
Name:		ruby-%{pkgname}
Version:	2.5.4
Release:	2
Group:		Development/Languages
# lib/test/unit/diff.rb is under GPLv2 or Ruby or Python
# lib/test-unit.rb is under LGPLv2+ or Ruby
# Other file: GPLv2 or Ruby
License:	(GPL v2 or Ruby) and (GPL v2 or Ruby or Python) and (LGPL v2+ or Ruby)
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	af76916d97034e9f4f8936ab1dc90b8f
URL:		http://rubyforge.org/projects/test-unit/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Test::Unit 2.x - Improved version of Test::Unit bundled in Ruby 1.8.x.
Ruby 1.9.x bundles minitest not Test::Unit. Test::Unit bundled in Ruby
1.8.x had not been improved but unbundled Test::Unit (Test::Unit 2.x)
will be improved actively.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
#rake test --trace
ruby -Ilib ./test/run-test.rb
%endif

rdoc --ri --op ri lib
rdoc --op rdoc lib
# rm -r ri/NOT_THIS_MODULE_RELATED_DIRS
rm ri/created.rid
rm ri/cache.ri
rm -r ri/Object

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{ruby_ridir},%{ruby_rdocdir}/%{name}-%{version}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.textile TODO
%{ruby_vendorlibdir}/test
%{ruby_vendorlibdir}/test-unit.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Test
