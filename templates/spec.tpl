%define debug_package %{nil}

Name:    {{name}}
Version: {{version}}
Release: 1%{?dist}
Summary: {{summary}}
License: {{license}}
URL:     {{URL}}

{%- for source in sources %}
Source{{loop.index - 1}}: {{source}}
{%- endfor %}

%{?systemd_requires}
Requires(pre): shadow-utils

%description

{{description}}

%prep
%setup -q -n {{name}}-%{version}.linux-amd64

%build
# Custom build from templating
{{build}}

%install
# Custom install from templating
{{install}}

%pre
# Custom pre from templating
{{pre}}

%post
# Custom post from templating
{{post}}

%preun
# Custom preun from templating
{{preun}}

%postun

# Custom postun from templating
{{postun}}

%files
# Custom files from templating
{{files}}
