%define debug_package %{nil}

Name:    jmx_exporter
Version: 0.9
Release: 1%{?dist}
BuildArch: noarch
Summary: Prometheus exporter for mBeans scrape and expose.
License: ASL 2.0
URL:     https://github.com/prometheus/jmx_exporter

Source0: http://search.maven.org/remotecontent?filepath=io/prometheus/jmx/jmx_prometheus_httpserver/%{version}/jmx_prometheus_httpserver-%{version}-jar-with-dependencies.jar 
Source1: jmx_exporter.service
Source2: jmx_exporter.default

#%{?systemd_requires}
#Requires(pre): shadow-utils
Requires: java

%description

A Collector that can configurably scrape and expose mBeans of a JMX target. It meant to be run as a Java Agent, exposing an HTTP server and scraping the local JVM.

%prep

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/share/prometheus/jmx_exporter
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 644 %{SOURCE0} %{buildroot}/usr/share/prometheus/jmx_exporter/jmx_exporter.jar
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/jmx_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/jmx_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post jmx_exporter.service

%preun
%systemd_preun jmx_exporter.service

%postun
%systemd_postun jmx_exporter.service

%files
%defattr(-,root,root,-)
/usr/share/prometheus/jmx_exporter/jmx_exporter.jar
/usr/lib/systemd/system/jmx_exporter.service
%config(noreplace) /etc/default/jmx_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
