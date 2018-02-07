%define debug_package %{nil}

Name:    postgres_exporter
Version: 0.4.1
Release: 1%{?dist}
Summary: Prometheus exporter for PostgreSQL server metrics
License: ASL 2.0
URL:     https://github.com/wrouesnel/postgres_exporter

Source0: https://github.com/wrouesnel/postgres_exporter/releases/download/v%{version}/postgres_exporter_v%{version}_linux-amd64.tar.gz
Source1: postgres_exporter.service
Source2: postgres_exporter.default



%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for PostgreSQL server metrics. Supported Postgres versions: 9.1 and up.

%prep
%setup -q -n postgres_exporter_v%{version}_linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 postgres_exporter %{buildroot}/usr/bin/postgres_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/postgres_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/postgres_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post postgres_exporter.service

%preun
%systemd_preun postgres_exporter.service

%postun
%systemd_postun postgres_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/postgres_exporter
/usr/lib/systemd/system/postgres_exporter.service
%config(noreplace) /etc/default/postgres_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
