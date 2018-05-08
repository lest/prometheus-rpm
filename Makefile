PACKAGES7 = prometheus \
prometheus2 \
alertmanager \
node_exporter \
mysqld_exporter \
postgres_exporter \
elasticsearch_exporter \
blackbox_exporter \
haproxy_exporter \
consul_exporter \
graphite_exporter \
jmx_exporter \
snmp_exporter \
apache_exporter \
redis_exporter \
collectd_exporter \
rabbitmq_exporter \
pushgateway \
sachet \
statsd_exporter

PACKAGES6 = node_exporter 

.PHONY: $(PACKAGES6)
.PHONY: $(PACKAGES7)

all: $(PACKAGES7) $(PACKAGES6)

6: $(PACKAGES6)

$(PACKAGES7):
	docker run --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		lest/centos7-rpm-builder \
		build-spec SOURCES/$@.spec
$(PACKAGES6):
	docker run --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist6:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist6:/rpmbuild/RPMS/noarch \
		quay.io/zoonage/centos6-rpm-build \
		build-spec SOURCES/$@.spec

sign:
	docker run --rm \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/bin:/rpmbuild/bin \
		-v ${PWD}/RPM-GPG-KEY-prometheus-rpm:/rpmbuild/RPM-GPG-KEY-prometheus-rpm \
		-v ${PWD}/secret.asc:/rpmbuild/secret.asc \
		-v ${PWD}/.passphrase:/rpmbuild/.passphrase \
		lest/centos7-rpm-builder \
		bin/sign
	docker run --rm \
		-v ${PWD}/_dist6:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/bin:/rpmbuild/bin \
		-v ${PWD}/RPM-GPG-KEY-prometheus-rpm:/rpmbuild/RPM-GPG-KEY-prometheus-rpm \
		-v ${PWD}/secret.asc:/rpmbuild/secret.asc \
		-v ${PWD}/.passphrase:/rpmbuild/.passphrase \
		quay.io/zoonage/centos6-rpm-build \
		bin/sign

publish: sign
	package_cloud push --skip-errors prometheus-rpm/release/el/7 _dist7/*.rpm
	package_cloud push --skip-errors prometheus-rpm/release/el/6 _dist6/*.rpm

clean:
	rm -rf _dist*
	rm -f **/*.tar.gz
	rm -f **/*.jar
