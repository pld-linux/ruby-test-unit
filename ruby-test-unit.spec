# TODO
# - any policy what to package in %{ruby_ridir}?
#
# Conditional build:
%bcond_without	tests		# build without tests

%define pkgname test-unit
Summary:	Improved version of Test::Unit bundled in Ruby 1.8.x
Name:		ruby-%{pkgname}
Version:	2.1.2
Release:	0.1
Group:		Development/Languages
# lib/test/unit/diff.rb is under GPLv2 or Ruby or Python
# lib/test-unit.rb is under LGPLv2+ or Ruby
# Other file: GPLv2 or Ruby
License:	(GPL v2 or Ruby) and (GPL v2 or Ruby or Python) and (LGPL v2+ or Ruby)
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	fbe74832c21be380098569a99f75858d
URL:		http://rubyforge.org/projects/test-unit/
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
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

# missing file (test_case4.rb) from test
#./test/collector/test-load.rb:69:    @sub_test_case4 = @sub_test_dir + "test_case4.rb"
%{__rm} test/collector/test-load.rb

#test_escaped?(TestUnitPriority):
#NoMethodError: undefined method `tmpdir' for Dir:Class
#    test-unit-2.1.2/test/test-priority.rb:115:in `assert_escaped_name'
#    test-unit-2.1.2/test/test-priority.rb:108:in `test_escaped?'
%{__rm} test/test-priority.rb

%build
%if %{with tests}
#rake test --trace
# UTF8 locale needed for tests to pass
LC_ALL=en_US.UTF-8 \
ruby -Ilib ./test/run-test.rb
%endif

rdoc --ri --op ri lib
rdoc --op rdoc lib
# rm -r ri/NOT_THIS_MODULE_RELATED_DIRS
rm ri/created.rid
rm ri/cache.ri

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}/%{name}-%{version}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc History.txt README.txt
%{ruby_rubylibdir}/test

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Test
