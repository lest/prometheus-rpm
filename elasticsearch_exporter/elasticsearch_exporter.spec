%define debug_package %{nil}

Name:    elasticsearch_exporter
Version: 1.0.1
Release: 1%{?dist}
Summary: Elasticsearch stats exporter for Prometheus
License: ASL 2.0
URL:     https://github.com/justwatchcom/elasticsearch_exporter

Source0: https://github.com/justwatchcom/elasticsearch_exporter/releases/download/v%{version}/elasticsearch_exporter-%{version}.linux-amd64.tar.gz
Source1: elasticsearch_exporter.service
Source2: elasticsearch_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Elasticsearch stats exporter for Prometheus.

%prep
%setup -q -n elasticsearch_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 elasticsearch_exporter %{buildroot}/usr/bin/elasticsearch_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/elasticsearch_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/elasticsearch_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post elasticsearch_exporter.service

%preun
%systemd_preun elasticsearch_exporter.service

%postun
%systemd_postun elasticsearch_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/elasticsearch_exporter
/usr/lib/systemd/system/elasticsearch_exporter.service
%config(noreplace) /etc/default/elasticsearch_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
