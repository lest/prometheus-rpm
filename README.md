# Prometheus RPM Packages

[![Build Status](https://travis-ci.org/lest/prometheus-rpm.svg?branch=master)](https://travis-ci.org/lest/prometheus-rpm)

The repository contains the files needed to build [Prometheus][1] RPM packages
for CentOS 7.

## Installing
The packages are available in [the packagecloud repository][2] and can be used
by adding the following `/etc/yum.repos.d/prometheus.repo`:

### CentOS 7
``` conf
[prometheus]
name=prometheus
baseurl=https://packagecloud.io/prometheus-rpm/release/el/7/$basearch
repo_gpgcheck=1
enabled=1
gpgkey=https://packagecloud.io/prometheus-rpm/release/gpgkey
       https://raw.githubusercontent.com/lest/prometheus-rpm/master/RPM-GPG-KEY-prometheus-rpm
gpgcheck=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
```
### CentOS 6
``` conf
[prometheus]
name=prometheus
baseurl=https://packagecloud.io/prometheus-rpm/release/el/6/$basearch
repo_gpgcheck=1
enabled=1
gpgkey=https://packagecloud.io/prometheus-rpm/release/gpgkey
       https://raw.githubusercontent.com/lest/prometheus-rpm/master/RPM-GPG-KEY-prometheus-rpm
gpgcheck=1
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
```

## Adding a new exporter
### Auto generation (CentOS 6 & 7)
1. Add a new section under `packages` in `templating.yaml` with the required information (overriding any defaults if required).
2. Create a new directory with the name of the exporter and populate it with a file named `<exporter_name>.default` which will contain the default environment variables passed to the init and unit files. 
3. Once this is done add this exporter to the list of `AUTO_GENERATED` expoters in `Makefile`.
4. Test that you can build this RPM using the command `make <exporter_name>`.

### Custom (CentOS 7 only)
1. Add the exporter to the list of `PACKAGES7` in the file `Makefile`.
2. Make a new directory with the same name as the exporter.
3. Populate this directory with all the required files to build the RPM.
4. Test that you can build this RPM using the command `make <exporter_name>`.

## Build RPMs manually

Build all packages with:

``` shell
make all
```

or build a single package only, e.g.:

``` shell
make node_exporter
```

The resulting RPMs will be created in the `_dist6` or `_dist7` directory depending on the version of CentOS that they were built for. builds in `_dist6` may also work for el5.

## Ansible role

An [Ansible][3] role which installs Prometheus packages from these RPMs is
available in [Github][4] or in [Galaxy][5].

[1]: https://prometheus.io
[2]: https://packagecloud.io/prometheus-rpm/release
[3]: https://www.ansible.com/
[4]: https://github.com/cogini/ansible-role-prometheus-rpm
[5]: https://galaxy.ansible.com/cogini/prometheus-rpm/
