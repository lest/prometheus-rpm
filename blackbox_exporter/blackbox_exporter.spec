%define debug_package %{nil}

Name:    blackbox_exporter
Version: 0.8.1
Release: 2%{?dist}
Summary: Blackbox prober exporter
License: ASL 2.0
URL:     https://github.com/prometheus/blackbox_exporter

Source0: https://github.com/prometheus/blackbox_exporter/releases/download/v%{version}/blackbox_exporter-%{version}.linux-amd64.tar.gz
Source1: blackbox_exporter.service
Source2: blackbox_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP and ICMP.

%prep
%setup -q -n blackbox_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/etc/prometheus
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 blackbox_exporter %{buildroot}/usr/bin/blackbox_exporter
install -m 644 blackbox.yml %{buildroot}/etc/prometheus/blackbox.yml
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/blackbox_exporter.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/blackbox_exporter

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post blackbox_exporter.service

%preun
%systemd_preun blackbox_exporter.service

%postun
%systemd_postun blackbox_exporter.service

%files
%defattr(-,root,root,-)
/usr/bin/blackbox_exporter
%config(noreplace) /etc/prometheus/blackbox.yml
/usr/lib/systemd/system/blackbox_exporter.service
%config(noreplace) /etc/default/blackbox_exporter
%attr(755, prometheus, prometheus)/var/lib/prometheus
