%define debug_package %{nil}

Name:    alertmanager
Version: 0.16.1
Release: 1%{?dist}
Summary: Prometheus Alertmanager.
License: ASL 2.0
URL:     https://github.com/prometheus/%{name}

Source0: https://github.com/prometheus/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

The Alertmanager handles alerts sent by client applications such as the
Prometheus server. It takes care of deduplicating, grouping, and routing them to
the correct receiver integration such as email, PagerDuty, or OpsGenie. It also
takes care of silencing and inhibition of alerts.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 644 alertmanager.yml %{buildroot}%{_sysconfdir}/prometheus/%{name}.yml
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 755 amtool %{buildroot}%{_bindir}/amtool
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

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
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yml
%{_bindir}/%{name}
%{_bindir}/amtool
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
