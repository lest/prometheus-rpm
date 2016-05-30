# Prometheus RPM Packages

The repository contains the files needed to build [Prometheus][1] RPM packages
for CentOS 7.

The packages are available on [Open Build Service][2] and can be used by adding
the following `/etc/yum.repos.d/prometheus.repo`:


``` conf
[prometheus]
name=Prometheus Packages (CentOS_7)
type=rpm-md
baseurl=http://download.opensuse.org/repositories/home:/justlest:/prometheus/CentOS_7/
gpgcheck=1
gpgkey=http://download.opensuse.org/repositories/home:/justlest:/prometheus/CentOS_7//repodata/repomd.xml.key
enabled=1
```

## Build RPMs manually

Build all packages with:

``` shell
make all
```

or build a single package only, e.g.:

``` shell
make node_exporter
```

The resulting RPMs will be created in the `_dist` directory.

[1]: https://prometheus.io
[2]: https://build.opensuse.org/project/show/home:justlest:prometheus
