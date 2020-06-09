%define debug_package %{nil}

Name:       exporter_exporter
Version:    0.4.0
Release:    0%{?dist}
Summary:    Simple reverse proxy for prometheus exporters
License:    ASL 2.0
URL:        https://github.com/QubitProducts/%{name}
Source0:    https://github.com/QubitProducts/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1:    %{name}.service
Source2:    %{name}.default
Source3:    exporter_exporter.yml

# Requires:   make

%description
A simple reverse proxy for prometheus exporters. It is intended as a single
binary alternative to nginx/apache for use in environments where opening
multiple TCP ports to all servers might be difficult (technically or
politically).

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
# mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/exporter_exporter.yml
mkdir %{buildroot}%{_sysconfdir}/prometheus/exporter_exporter.d

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
%config(noreplace) %attr(644, root, root)%{_sysconfdir}/prometheus/exporter_exporter.yml
%dir %{_sysconfdir}/prometheus/exporter_exporter.d
