%define debug_package %{nil}

Name:		 prometheus
Version: 1.8.2
Release: 1%{?dist}
Summary: The Prometheus monitoring system and time series database.
License: ASL 2.0
URL:     https://prometheus.io

Source0: https://github.com/prometheus/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%description

Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/%{name}
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 755 promtool %{buildroot}%{_bindir}/promtool
for dir in console_libraries consoles; do
  for file in ${dir}/*; do
    install -D -m 644 ${file} %{buildroot}%{_datarootdir}/%{name}/${file}
  done
done
install -D -m 644 %{name}.yml %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
          -c "Prometheus services" %{name}
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
%{_bindir}/promtool
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yml
%{_datarootdir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%attr(755, %{name}, %{name})%{_sharedstatedir}/%{name}
