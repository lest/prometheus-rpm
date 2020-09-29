%define debug_package %{nil}

Name:       ssl_exporter
Version:    2.1.1
Release:    1%{?dist}
Summary:    Prometheus exporter for SSL certificates.
License:    ASL 2.0
URL:        https://github.com/ribbybibby/ssl_exporter

Source0:    https://github.com/ribbybibby/ssl_exporter/releases/download/v%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1:    %{name}.service
Source2:    %{name}.default
Source3:    %{name}.yml

# Requires:   make

%description
Prometheus exporter for SSL certificates.

%prep
%setup -q -D -c %{name}_%{version}_linux_amd64

%build
/bin/true

%install
# mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/ssl_exporter.yml

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
%config(noreplace) %attr(644, root, root)%{_sysconfdir}/prometheus/ssl_exporter.yml
