%define debug_package %{nil}
%define user prometheus
%define group prometheus

Name:    couchbase_exporter
Version: 0.9.6
Release: 1%{?dist}
Summary: Prometheus exporter for Couchbase server metrics.
License: ASL 2.0
URL:     https://github.com/blakelead/couchbase_exporter

Source0: https://github.com/blakelead/couchbase_exporter/releases/download/%{version}/%{name}-%{version}-linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default
Source3: %{name}.yml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Prometheus exporter for Couchbase server metrics.

%prep
%setup -q -D -c %{name}-%{version}-linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}/opt/%{name}/%{name}
find metrics/ -name '*.json' -type f -exec install -Dm 0644 "{}" %{buildroot}/opt/%{name}/{} \;
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.yml
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

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
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
/opt/%{name}/%{name}
%dir %attr(755, %{user}, %{group}) /opt/%{name}/metrics
%attr(-, %{user}, %{group}) /opt/%{name}/metrics/*
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.yml
%{_unitdir}/%{name}.service
