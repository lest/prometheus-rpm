%define debug_package %{nil}

Name:    junos_exporter
Version: 0.9.8
Release: 1%{?dist}
Summary: Prometheus exporter for Junos device metrics
License: MIT
URL:     https://github.com/czerwonk/%{name}

Source0: https://github.com/czerwonk/%{name}/releases/download/%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default
Source3: %{name}.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for Junos device metrics.

%prep
%setup -q -c -n %{name}_%{version}_linux_amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yaml

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
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yaml
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
