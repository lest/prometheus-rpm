%define debug_package %{nil}

Name:    haproxy_exporter
Version: 0.8.0
Release: 1%{?dist}
Summary: Haproxy exporter
License: ASL 2.0
URL:     https://github.com/prometheus/haproxy_exporter

Source0: https://github.com/prometheus/haproxy_exporter/releases/download/v%{version}/haproxy_exporter-%{version}.linux-amd64.tar.gz
Source1: haproxy_exporter.service
Source2: haproxy_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Simple server that scrapes HAProxy stats and exports them via HTTP for Prometheus consumption

%prep
%setup -q -n haproxy_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 haproxy_exporter %{buildroot}/usr/bin/haproxy_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/haproxy_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/haproxy_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post haproxy_exporter.service

%preun
%systemd_preun haproxy_exporter.service

%postun
%systemd_postun haproxy_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/haproxy_exporter
/usr/lib/systemd/system/haproxy_exporter.service
%config(noreplace) /etc/default/haproxy_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
