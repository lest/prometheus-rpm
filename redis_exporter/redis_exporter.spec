%define debug_package %{nil}

Name:    redis_exporter
Version: v0.14
Release: 1%{?dist}
Summary: Redis stats exporter for Prometheus
License: MIT
URL:     https://github.com/oliver006/redis_exporter

Source0: https://github.com/oliver006/redis_exporter/releases/download/%{version}/redis_exporter-%{version}.linux-amd64.tar.gz
Source1: redis_exporter.service
Source2: redis_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Redis stats exporter for Prometheus.

%prep
%setup -q -c -n redis_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 redis_exporter %{buildroot}/usr/bin/redis_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/redis_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/redis_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post redis_exporter.service

%preun
%systemd_preun redis_exporter.service

%postun
%systemd_postun redis_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/redis_exporter
/usr/lib/systemd/system/redis_exporter.service
%config(noreplace) /etc/default/redis_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
