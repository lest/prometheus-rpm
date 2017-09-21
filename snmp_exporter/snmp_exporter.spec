%define debug_package %{nil}

Name:    snmp_exporter
Version: 0.6.0
Release: 1%{?dist}
Summary: Prometheus SNMP exporter.
License: ASL 2.0
URL:     https://github.com/prometheus/snmp_exporter

Source0: https://github.com/prometheus/snmp_exporter/releases/download/v%{version}/snmp_exporter-%{version}.linux-amd64.tar.gz
Source1: snmp_exporter.service
Source2: snmp_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

This is an exporter that exposes information gathered from SNMP for use by the Prometheus monitoring system.

%prep
%setup -q -n snmp_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 snmp_exporter %{buildroot}/usr/bin/snmp_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/snmp_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/snmp_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post snmp_exporter.service

%preun
%systemd_preun snmp_exporter.service

%postun
%systemd_postun snmp_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/snmp_exporter
/usr/lib/systemd/system/snmp_exporter.service
%config(noreplace) /etc/default/snmp_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
