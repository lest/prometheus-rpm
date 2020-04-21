%define debug_package %{nil}

Name:	 thanos
Version: 0.12.1
Release: 1%{?dist}
Summary: Highly available Prometheus setup with long term storage capabilities.
License: ASL 2.0
URL:     https://github.com/improbable-eng/thanos
Conflicts: prometheus

Source0: https://github.com/thanos-io/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: thanos-sidecar.service
Source2: thanos-sidecar.default
Source3: thanos-store.service
Source4: thanos-store.default
Source5: thanos-query.service
Source6: thanos-query.default
Source7: thanos-compact.service
Source8: thanos-compact.default
Source9: thanos-rule.service
Source10: thanos-rule.default
Source11: thanos_alerts.yml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Thanos is a set of components that can be composed into a highly available
metric system with unlimited storage capacity, which can be added seamlessly on
top of existing Prometheus deployments.

Thanos leverages the Prometheus 2.0 storage format to cost-efficiently store
historical metric data in any object storage while retaining fast query
latencies. Additionally, it provides a global query view across all Prometheus
installations and can merge data from Prometheus HA pairs on the fly.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 thanos %{buildroot}%{_bindir}/thanos
for dir in store rule; do
    install -D -m 755 -d %{buildroot}%{_sharedstatedir}/%{name}/${dir}
done
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/thanos-sidecar.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/thanos-sidecar
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/thanos-store.service
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/default/thanos-store
install -D -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/thanos-query.service
install -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/default/thanos-query
install -D -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/thanos-compact.service
install -D -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/default/thanos-compact
install -D -m 644 %{SOURCE9} %{buildroot}%{_unitdir}/thanos-rule.service
install -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/default/thanos-rule
install -D -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/prometheus/thanos_alerts.yml

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post thanos-sidecar.service
%systemd_post thanos-store.service
%systemd_post thanos-query.service
%systemd_post thanos-compact.service
%systemd_post thanos-rule.service

%preun
%systemd_preun thanos-sidecar.service
%systemd_preun thanos-store.service
%systemd_preun thanos-query.service
%systemd_preun thanos-compact.service
%systemd_preun thanos-rule.service

%postun
%systemd_postun thanos-sidecar.service
%systemd_postun thanos-store.service
%systemd_postun thanos-query.service
%systemd_postun thanos-compact.service
%systemd_postun thanos-rule.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/thanos-sidecar.service
%{_unitdir}/thanos-store.service
%{_unitdir}/thanos-query.service
%{_unitdir}/thanos-compact.service
%{_unitdir}/thanos-rule.service
%config(noreplace) %{_sysconfdir}/default/thanos-sidecar
%config(noreplace) %{_sysconfdir}/default/thanos-store
%config(noreplace) %{_sysconfdir}/default/thanos-query
%config(noreplace) %{_sysconfdir}/default/thanos-compact
%config(noreplace) %{_sysconfdir}/default/thanos-rule
%config(noreplace) %{_sysconfdir}/prometheus/thanos_alerts.yml
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/%{name}
%dir %attr(750, prometheus, prometheus)%{_sharedstatedir}/%{name}/store
%dir %attr(750, prometheus, prometheus)%{_sharedstatedir}/%{name}/rule
