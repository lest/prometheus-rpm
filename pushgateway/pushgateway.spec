%define debug_package %{nil}

Name:		 pushgateway
Version: 0.4.0
Release: 1%{?dist}
Summary: Prometheus Pushgateway.
License: ASL 2.0
URL:     https://github.com/prometheus/pushgateway

Source0: https://github.com/prometheus/pushgateway/releases/download/v%{version}/pushgateway-%{version}.linux-amd64.tar.gz
Source1: pushgateway.service
Source2: pushgateway.default

%description

The Prometheus Pushgateway exists to allow ephemeral and batch jobs to expose their metrics to Prometheus.
Since these kinds of jobs may not exist long enough to be scraped, they can instead push their metrics to
a Pushgateway. The Pushgateway then exposes these metrics to Prometheus.

%prep
%setup -q -n pushgateway-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 pushgateway %{buildroot}/usr/bin/pushgateway
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/pushgateway.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/pushgateway

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post pushgateway.service

%preun
%systemd_preun pushgateway.service

%postun
%systemd_postun pushgateway.service

%files
%defattr(-,root,root,-)
/usr/bin/pushgateway
/usr/lib/systemd/system/pushgateway.service
%config(noreplace) /etc/default/pushgateway
