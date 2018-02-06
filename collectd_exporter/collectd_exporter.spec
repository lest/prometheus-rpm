%define debug_package %{nil}

Name:    collectd_exporter
Version: 0.4.0
Release: 1%{?dist}
Summary: Collectd stats exporter for Prometheus
License: ASL 2.0
URL:     https://github.com/prometheus/collectd_exporter

Source0: https://github.com/prometheus/collectd_exporter/releases/download/v%{version}/collectd_exporter-%{version}.linux-amd64.tar.gz
Source1: collectd_exporter.service
Source2: collectd_exporter.default



%{?systemd_requires}
Requires(pre): shadow-utils

%description

Collectd stats exporter for Prometheus. It accepts collectd's binary network
protocol as sent by collectd's network plugin and metrics in JSON format via
HTTP POST as sent by collectd's write_http plugin, and transforms and exposes
them for consumption by Prometheus.

%prep
%setup -q -c -n collectd_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 collectd_exporter %{buildroot}/usr/bin/collectd_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/collectd_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/collectd_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post collectd_exporter.service

%preun
%systemd_preun collectd_exporter.service

%postun
%systemd_postun collectd_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/collectd_exporter
/usr/lib/systemd/system/collectd_exporter.service
%config(noreplace) /etc/default/collectd_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
