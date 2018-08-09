Name:       sachet
Version:    0.0.8
Release:    1%{?dist}
Summary:    SMS alerts for Prometheus Alertmanager
License:    BSD
URL:        https://github.com/messagebird/%{name}
Source0:    https://github.com/messagebird/%{name}/releases/download/%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1:    %{name}.service
Source2:    %{name}.default
Source3:    %{name}.yml

Requires:   make

%description
Sachet (or सचेत) is Hindi for conscious. Sachet is an SMS alerting tool for the Prometheus Alertmanager.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yml

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yml
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
