%define debug_package %{nil}

Name:    openstack_exporter
Version: 1.1.0
Release: 1%{?dist}
Summary: Prometheus exporter for OpenStack metrics
License: MIT
URL:     https://github.com/openstack-exporter/openstack-exporter

Source0: https://github.com/openstack-exporter/openstack-exporter/releases/download/v%{version}/openstack-exporter-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default
Source3: %{name}_clouds.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
A OpenStack exporter for prometheus written in Golang using the gophercloud library.

%prep
%setup -q -n openstack-exporter-%{version}.linux-amd64

%build
/bin/true

%install
install -D -m 755 openstack-exporter %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}_clouds.yaml

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
%config(noreplace) %attr(640, root, prometheus)%{_sysconfdir}/prometheus/%{name}_clouds.yaml
