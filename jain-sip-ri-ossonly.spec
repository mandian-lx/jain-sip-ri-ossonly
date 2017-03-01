%{?_javapackages_macros:%_javapackages_macros}

#
# FIXME: javadoc fails:
#        Exit code: 1 - javadoc: error - Illegal package name: "ant-tasks.src.net.java.jsip.ant.tasks"
#

Summary:	The official Reference Implementation of the JAIN SIP API witch only OSS code 
Name:		jain-sip-ri-ossonly
Version:	1.2.279
Release:	1
License:	Public Domain
Group:		Development/Java
Url:		https://github.com/jitsi/jain-sip
Source0:	https://github.com/jitsi/jain-sip/archive/v%{version}-jitsi-oss1/%{name}-%{version}.tar.gz
BuildArch: 	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(log4j:log4j)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:	mvn(org.opentelecoms.sip:sip-api-1.2)
BuildRequires:	mvn(org.opentelecoms.sdp:sdp-api)

%description
Package of JAIN SIP and SDP that contains only OSS code
(i.e. not javax.sip/java.sdp).

%files -f .mfiles
%doc README
%doc README-DISTRIBUTION
%doc contributing.txt
%doc TODO.txt
%doc licenses/README.txt
%doc licenses/NIST-CONDITIONS-OF-USE.txt
%doc licenses/JSIP\ Spec\ License.pdf

#----------------------------------------------------------------------------
#
#package javadoc
#Summary: Javadoc for %{name}
#
#description javadoc
#API documentation for %{name}.
#
#files javadoc -f .mfiles-javadoc
#
#----------------------------------------------------------------------------

%prep
%setup -q -n jain-sip-%{version}-jitsi-oss1
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Fix version
%pom_xpath_replace "pom:project/pom:version" "<version>%{version}</version>" m2/%{name}

# Fix excludes
%pom_xpath_remove "pom:plugin[pom:artifactId[./text()='maven-compiler-plugin']]/pom:configuration/pom:excludes" m2/%{name}

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin m2/%{name} "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -j -- -f m2/%{name}/pom.xml -Dproject.build.sourceEncoding=ISO-8859-1 -Dmaven.compiler.source=1.7 -Dmaven.compiler.target=1.7

%install
%mvn_install -- -f m2/%{name}/pom.xml 

