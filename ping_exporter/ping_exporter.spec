%global debug_package %{nil}

Name:    ping_exporter
Version: 0.4.6
Release: 2%{?dist}
Summary: Ping exporter
License: ASL 2.0
URL:        https://github.com/jaxxstorm/ping_exporter
Source0:    https://github.com/jaxxstorm/ping_exporter/releases/download/%{version}/ping_exporter-%{version}.Linux-x86_64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

The ping exporter allows ping probing of endpoints via ICMP.

%prep
%setup -q -n %{name}-%{version}.Linux-x86_64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
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
%caps(cap_net_raw=ep) %{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
