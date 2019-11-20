%define debug_package %{nil}

Name:	 promtail
Version: 1.0.0
Release: 1%{?dist}
Summary: Loki promtail agent.
License: ASL 2.0
URL:     https://github.com/grafana/%{name}

Source0: https://github.com/grafana/loki/releases/download/v%{version}/%{name}-linux-amd64.gz
Source1: %{name}.service
Source2: %{name}.default
Source3: %{name}.yml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Promtail is an agent which ships the contents of local logs to a private
Loki instance or Grafana Cloud.

%prep
%setup -q -T -c -n %{name}-linux-amd64
gunzip -d -N -c -v ../../SOURCES/%{name}-linux-amd64.gz > %{name}-linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 %{name}-linux-amd64 %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml

%pre
getent group promtail >/dev/null || groupadd -r promtail
getent passwd promtail >/dev/null || \
  useradd -r -g promtail -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
          -c "Promtail services" promtail 
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
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yml
%dir %attr(750, promtail, promtail)%{_sharedstatedir}/%{name}
