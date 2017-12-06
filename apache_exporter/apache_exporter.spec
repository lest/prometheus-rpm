%define debug_package %{nil}

Name:    apache_exporter
Version: 0.5.0
Release: 1%{?dist}
Summary: Prometheus exporter for apache mod_status statistics
License: MIT
URL:     https://github.com/Lusitaniae/apache_exporter

Source0: https://github.com/Lusitaniae/apache_exporter/releases/download/v%{version}/apache_exporter-%{version}.linux-amd64.tar.gz
Source1: apache_exporter.service
Source2: apache_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for apache mod_status statistics

%prep
%setup -q -n apache_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 apache_exporter %{buildroot}/usr/bin/apache_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/apache_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/apache_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post apache_exporter.service

%preun
%systemd_preun apache_exporter.service

%postun
%systemd_postun apache_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/apache_exporter
/usr/lib/systemd/system/apache_exporter.service
%config(noreplace) /etc/default/apache_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
