%define debug_package %{nil}
%define pkg_version 3.0.0-rc44
%define version 3.0.0rc44

Name:    mtail
Version: %{version}
Release: 1%{?dist}
Summary: Extract metrics from application logs
License: ASL 2.0
URL:     https://github.com/google/%{name}

Source0: https://github.com/google/%{name}/releases/download/v%{pkg_version}/%{name}_%{pkg_version}_Linux_arm64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Extract metrics from application logs to be exported into a timeseries database or timeseries calculator for alerting and dashboarding.

%prep
%setup -q -D -c %{name}

%build
/bin/true

%install
install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/prometheus/%{name}.d
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

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
%dir %{_sysconfdir}/prometheus/%{name}.d
%dir %{_localstatedir}/log/%{name}
