%global pkg_name maven-site-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        3.2
Release:        7.13%{?dist}
Summary:        Maven Site Plugin

License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-site-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

Patch0:         0001-Port-to-jetty-9.patch
Patch1:         0001-Fix-jetty-dependencies.patch
# Jetty is needed only in interactive mode of maven-site-plugin. Change
# dependency scope from compile to provided to reduce dependency bloat.
Patch2:         %{pkg_name}-jetty-provided.patch

BuildArch: noarch

BuildRequires: %{?scl_prefix}maven-local
BuildRequires: %{?scl_prefix}maven-artifact-manager
BuildRequires: %{?scl_prefix}maven-plugin-plugin
BuildRequires: %{?scl_prefix}maven-assembly-plugin
BuildRequires: %{?scl_prefix}maven-compiler-plugin
BuildRequires: %{?scl_prefix}maven-install-plugin
BuildRequires: %{?scl_prefix}maven-javadoc-plugin
BuildRequires: %{?scl_prefix}maven-jar-plugin
BuildRequires: %{?scl_prefix}maven-resources-plugin
BuildRequires: %{?scl_prefix}maven-doxia-sink-api
BuildRequires: %{?scl_prefix}maven-doxia-logging-api
BuildRequires: %{?scl_prefix}maven-doxia-core
BuildRequires: %{?scl_prefix}maven-doxia-module-xhtml
BuildRequires: %{?scl_prefix}maven-doxia-module-apt
BuildRequires: %{?scl_prefix}maven-doxia-module-xdoc
BuildRequires: %{?scl_prefix}maven-doxia-module-fml
BuildRequires: %{?scl_prefix}maven-doxia-sitetools
BuildRequires: %{?scl_prefix}maven-doxia-tools >= 1.4-8
BuildRequires: %{?scl_prefix}maven-project
BuildRequires: %{?scl_prefix}maven-surefire-plugin
BuildRequires: %{?scl_prefix}maven-surefire-provider-junit
BuildRequires: %{?scl_prefix}maven-shade-plugin
BuildRequires: %{?scl_prefix}maven-plugin-testing-harness
BuildRequires: %{?scl_prefix}maven-wagon-provider-api
BuildRequires: %{?scl_prefix}maven-reporting-exec
BuildRequires: %{?scl_prefix}plexus-containers-component-metadata
BuildRequires: %{?scl_prefix_java_common}jetty-client >= 9.0.0-0.1.RC0
BuildRequires: %{?scl_prefix_java_common}jetty-server >= 9.0.0-0.1.RC0
BuildRequires: %{?scl_prefix_java_common}jetty-servlet >= 9.0.0-0.1.RC0
BuildRequires: %{?scl_prefix_java_common}jetty-util >= 9.0.0-0.1.RC0
BuildRequires: %{?scl_prefix_java_common}jetty-webapp >= 9.0.0-0.1.RC0
BuildRequires: %{?scl_prefix_java_common}tomcat-servlet-3.0-api
BuildRequires: %{?scl_prefix}plexus-archiver
BuildRequires: %{?scl_prefix}plexus-containers-container-default
BuildRequires: %{?scl_prefix}plexus-i18n
BuildRequires: %{?scl_prefix}plexus-velocity
BuildRequires: %{?scl_prefix}plexus-utils
BuildRequires: %{?scl_prefix}jetty-parent


%description
The Maven Site Plugin is a plugin that generates a site for the current project.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p1
%patch1 -p1
%patch2
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# skipping tests because we need to fix them first for jetty update
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 3.2-7.13
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 3.2-7.12
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 3.2-7.11
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.10
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 3.2-7.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 3.2-7.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.7
- Mass rebuild 2014-05-26

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 3.2-7.6
- Adjust maven-wagon R/BR

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.4
- Mass rebuild 2014-02-18

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-7.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.2-7
- Mass rebuild 2013-12-27

* Wed Nov 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-6
- Remove BR on main jetty package

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-5
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Mar  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-4
- Merge branch 'port-to-jetty-9' into master

* Tue Feb 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-3
- Change jetty dependency scope to provided

* Mon Feb 25 2013 Michal Srb <msrb@redhat.com> - 3.2-3
- Port to jetty 9.0.0

* Thu Feb 07 2013 Michal Srb <msrb@redhat.com> - 3.2-2
- Migrate from maven-doxia to doxia subpackages

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2-1
- Update to upstream version 3.2
- Build with xmvn

* Tue Oct 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-3
- Don't require full jetty, only minimal set of subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-1
- Updatw to upstream 3.1

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 3.0-5
- BR/R servlet 3.

* Thu Jan 26 2012 Alexander Kurtakov <akurtako@redhat.com> 3.0-4
- Add BR/R on jetty-parent.

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-3
- Port for jetty 8.1.0
- Small spec cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Alexander Kurtakov <akurtako@redhat.com> 3.0-1
- Update to upstream 3.0 release.

* Thu Jul 21 2011 Jaromir Capik <jcapik@redhat.com> - 2.3-3
- Removal of plexus-maven-plugin dependency (not needed)

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3-2
- Add several missing things to (Build)Requires
- Fix build for maven3-only buildroot

* Wed May 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3-1
- Update to new upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2-1
- Update to new upstream version.

* Tue Jun 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-3
- Requires maven-doxia-tools.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-2
- Fix requires.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1-1
- Initial package.
