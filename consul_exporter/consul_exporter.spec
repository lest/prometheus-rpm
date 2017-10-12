%define debug_package %{nil}

Name:    consul_exporter
Version: 0.3.0
Release: 1%{?dist}
Summary: Prometheus Consul exporter.
License: ASL 2.0
URL:     https://github.com/prometheus/consul_exporter

Source0: https://github.com/prometheus/consul_exporter/releases/download/v%{version}/consul_exporter-%{version}.linux-amd64.tar.gz
Source1: consul_exporter.service
Source2: consul_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Export Consul service health to Prometheus.

%prep
%setup -q -n consul_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 consul_exporter %{buildroot}/usr/bin/consul_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/consul_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/consul_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post consul_exporter.service

%preun
%systemd_preun consul_exporter.service

%postun
%systemd_postun consul_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/consul_exporter
/usr/lib/systemd/system/consul_exporter.service
%config(noreplace) /etc/default/consul_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
