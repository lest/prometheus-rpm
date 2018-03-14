%define debug_package %{nil}

Name:    rabbitmq_exporter
Version: 0.26.0
Release: 1%{?dist}
Summary: Prometheus exporter for RabbitMQ metrics
License: MIT
URL:     https://github.com/kbudde/rabbitmq_exporter

Source0: https://github.com/kbudde/rabbitmq_exporter/releases/download/v%{version}/rabbitmq_exporter-%{version}.linux-amd64.tar.gz
Source1: rabbitmq_exporter.service
Source2: rabbitmq_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for RabbitMQ metrics.

%prep
%setup -q -n rabbitmq_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 rabbitmq_exporter %{buildroot}/usr/bin/rabbitmq_exporter
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/rabbitmq_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/rabbitmq_exporter

%pre
getent group prometheus >/dev/null || groupadd --system prometheus
getent passwd prometheus >/dev/null || \
  useradd --system --gid=prometheus --home=/var/lib/prometheus --shell=/sbin/nologin \
          --comment="Prometheus services" prometheus
exit 0

%post
%systemd_post rabbitmq_exporter.service

%preun
%systemd_preun rabbitmq_exporter.service

%postun
%systemd_postun rabbitmq_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/rabbitmq_exporter
/usr/lib/systemd/system/rabbitmq_exporter.service
%config(noreplace) /etc/default/rabbitmq_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
