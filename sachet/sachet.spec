Name:       sachet  
Version:    0.0.5
Release:    1%{?dist}
Summary:    SMS alerts for Prometheus Alertmanager
License:    BSD 
URL:        https://github.com/messagebird/sachet
Source0:    https://github.com/messagebird/sachet/releases/download/%{version}/sachet-%{version}.linux-amd64.tar.gz
Source1:    sachet.service
Source2:    sachet.default
Source3:    sachet.yml

BuildRequires:  golang  
Requires:   make    

%description
Sachet (or सचेत) is Hindi for conscious. Sachet is an SMS alerting tool for the Prometheus Alertmanager.

%prep
%setup -q -n sachet-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/etc/prometheus
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 sachet %{buildroot}%{_bindir}/
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/sachet.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/sachet
install -m 640 %{SOURCE3} %{buildroot}/etc/prometheus/sachet.yml

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post sachet.service

%preun
%systemd_preun sachet.service

%postun
%systemd_postun sachet.service

%files
%{_bindir}/sachet
%doc
/usr/lib/systemd/system/sachet.service
%config(noreplace) /etc/default/sachet
%config(noreplace) /etc/prometheus/sachet.yml
%attr(755, prometheus, prometheus)/var/lib/prometheus
