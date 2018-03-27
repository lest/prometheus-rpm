%define debug_package %{nil}

Name:    statsd_exporter
Version: 0.6.0
Release: 1%{?dist}
Summary: Prometheus StatsD exporter.
License: ASL 2.0
URL:     https://github.com/prometheus/statsd_exporter

Source0: https://github.com/prometheus/statsd_exporter/releases/download/v%{version}/statsd_exporter-%{version}.linux-amd64.tar.gz
Source1: statsd_exporter.service
Source2: statsd_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Export StatsD metrics in Prometheus format.

%prep
%setup -q -n statsd_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 statsd_exporter %{buildroot}/usr/bin/statsd_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/statsd_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/statsd_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post statsd_exporter.service

%preun
%systemd_preun statsd_exporter.service

%postun
%systemd_postun statsd_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/statsd_exporter
/usr/lib/systemd/system/statsd_exporter.service
%config(noreplace) /etc/default/statsd_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
