%define debug_package %{nil}

Name:    mysqld_exporter
Version: 0.9.0
Release: 1%{?dist}
Summary: Prometheus exporter for MySQL server metrics.
License: ASL 2.0
URL:     https://github.com/prometheus/mysqld_exporter

Source0: https://github.com/prometheus/mysqld_exporter/releases/download/v%{version}/mysqld_exporter-%{version}.linux-amd64.tar.gz
Source1: mysqld_exporter.service
Source2: mysqld_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for MySQL server metrics.

%prep
%setup -q -n mysqld_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 mysqld_exporter %{buildroot}/usr/bin/mysqld_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/mysqld_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/mysqld_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post mysqld_exporter.service

%preun
%systemd_preun mysqld_exporter.service

%postun
%systemd_postun mysqld_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/mysqld_exporter
/usr/lib/systemd/system/mysqld_exporter.service
%config(noreplace) /etc/default/mysqld_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
