%define debug_package %{nil}

Name:	 process_exporter
Version: 0.6.0
Release: 4%{?dist}
Summary: Process exporter for Prometheus.
License: MIT
URL:     https://github.com/ncabatoff/process-exporter
Conflicts: prometheus

Source0: https://github.com/ncabatoff/process-exporter/releases/download/v%{version}/process-exporter-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default
Source3: %{name}.yml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Prometheus exporter that mines /proc to report on selected processes.

%prep
%setup -q -n process-exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sysconfdir}/prometheus
install -D -m 755 process-exporter %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yml

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
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yml
