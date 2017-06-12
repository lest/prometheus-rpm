%define debug_package %{nil}

Name:		 alertmanager
Version: 0.7.1
Release: 1%{?dist}
Summary: Prometheus Alertmanager.
License: ASL 2.0
URL:     https://github.com/prometheus/alertmanager

Source0: https://github.com/prometheus/alertmanager/releases/download/v%{version}/alertmanager-%{version}.linux-amd64.tar.gz
Source1: alertmanager.service
Source2: alertmanager.default

%description

The Alertmanager handles alerts sent by client applications such as the
Prometheus server. It takes care of deduplicating, grouping, and routing them to
the correct receiver integration such as email, PagerDuty, or OpsGenie. It also
takes care of silencing and inhibition of alerts.

%prep
%setup -q -n alertmanager-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/etc/prometheus
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 alertmanager %{buildroot}/usr/bin/alertmanager
install -m 644 simple.yml %{buildroot}/etc/prometheus/alertmanager.yml
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/alertmanager.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/alertmanager

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post alertmanager.service

%preun
%systemd_preun alertmanager.service

%postun
%systemd_postun alertmanager.service

%files
%defattr(-,root,root,-)
/usr/bin/alertmanager
%config(noreplace) /etc/prometheus/alertmanager.yml
/usr/lib/systemd/system/alertmanager.service
%config(noreplace) /etc/default/alertmanager
%attr(755, prometheus, prometheus)/var/lib/prometheus
