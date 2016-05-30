%define debug_package %{nil}

Name:    node_exporter
Version: 0.12.0
Release: 1%{?dist}
Summary: Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
License: ASL 2.0
URL:     https://github.com/prometheus/node_exporter

Source0: https://github.com/prometheus/node_exporter/releases/download/%{version}/node_exporter-%{version}.linux-amd64.tar.gz
Source1: node_exporter.service
Source2: node_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n node_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 node_exporter %{buildroot}/usr/bin/node_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/node_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/node_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post node_exporter.service

%preun
%systemd_preun node_exporter.service

%postun
%systemd_postun node_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/node_exporter
/usr/lib/systemd/system/node_exporter.service
%config(noreplace) /etc/default/node_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
