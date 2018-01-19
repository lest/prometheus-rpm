%define debug_package %{nil}

Name:		 prometheus2
Version: 2.1.0
Release: 1%{?dist}
Summary: The Prometheus 2.1 monitoring system and time series database.
License: ASL 2.0
URL:     https://prometheus.io
Conflicts: prometheus

Source0: https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1: prometheus.service
Source2: prometheus.default

%description

Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

%prep
%setup -q -n prometheus-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/etc/prometheus
mkdir -vp %{buildroot}/usr/share/prometheus/console_libraries
mkdir -vp %{buildroot}/usr/share/prometheus/consoles
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 prometheus %{buildroot}/usr/bin/prometheus
install -m 755 promtool %{buildroot}/usr/bin/promtool
for dir in console_libraries consoles; do
  for file in ${dir}/*; do
    install -m 644 ${file} %{buildroot}/usr/share/prometheus/${file}
  done
done
install -m 644 prometheus.yml %{buildroot}/etc/prometheus/prometheus.yml
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/prometheus.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/prometheus

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post prometheus.service

%preun
%systemd_preun prometheus.service

%postun
%systemd_postun prometheus.service

%files
%defattr(-,root,root,-)
/usr/bin/prometheus
/usr/bin/promtool
%config(noreplace) /etc/prometheus/prometheus.yml
/usr/share/prometheus
/usr/lib/systemd/system/prometheus.service
%config(noreplace) /etc/default/prometheus
%attr(755, prometheus, prometheus)/var/lib/prometheus
