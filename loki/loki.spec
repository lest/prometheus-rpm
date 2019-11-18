%define debug_package %{nil}

Name:	 loki
Version: 0.4.0
Release: 1%{?dist}
Summary: Horizontally-scalable, highly-available, multi-tenant log aggregation system.
License: ASL 2.0
URL:     https://github.com/grafana/%{name}

Source0: https://github.com/grafana/%{name}/releases/download/v%{version}/%{name}-linux-amd64.gz
Source1: %{name}.service
Source2: %{name}.default
Source3: %{name}.yml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Grafana Loki is a set of components that can be composed into a fully
featured logging stack.

Unlike other logging systems, Loki is built around the idea of only
indexing labels for logs and leaving the original log message unindexed.
This means that Loki is cheaper to operate and can be orders of
magnitude more efficient.

%prep
%setup -q -T -c -n %{name}-linux-amd64
gunzip -d -N -c -v ../../SOURCES/%{name}-linux-amd64.gz > %{name}-linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 %{name}-linux-amd64 %{buildroot}%{_bindir}/%{name}
for dir in chunks index; do
    install -D -m 755 -d %{buildroot}%{_sharedstatedir}/%{name}/${dir}
done
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml

%pre
getent group loki >/dev/null || groupadd -r loki
getent passwd loki >/dev/null || \
  useradd -r -g loki -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
          -c "Loki services" loki
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
%dir %attr(750, loki, loki)%{_sharedstatedir}/%{name}
%dir %attr(750, loki, loki)%{_sharedstatedir}/%{name}/chunks
%dir %attr(750, loki, loki)%{_sharedstatedir}/%{name}/index
