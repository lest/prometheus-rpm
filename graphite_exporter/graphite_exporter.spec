%define debug_package %{nil}

Name:    graphite_exporter
Version: 0.2.0
Release: 1%{?dist}
Summary: Prometheus Graphite exporter.
License: ASL 2.0
URL:     https://github.com/prometheus/graphite_exporter

Source0: https://github.com/prometheus/graphite_exporter/releases/download/v%{version}/graphite_exporter-%{version}.linux-amd64.tar.gz
Source1: graphite_exporter.service
Source2: graphite_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

An exporter for metrics exported in the Graphite plaintext protocol. It accepts data over both TCP and UDP, and transforms and exposes them for consumption by Prometheus.

%prep
%setup -q -n graphite_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 graphite_exporter %{buildroot}/usr/bin/graphite_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/graphite_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/graphite_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post graphite_exporter.service

%preun
%systemd_preun graphite_exporter.service

%postun
%systemd_postun graphite_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/graphite_exporter
/usr/lib/systemd/system/graphite_exporter.service
%config(noreplace) /etc/default/graphite_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
