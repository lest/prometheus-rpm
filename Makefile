PACKAGES7 = prometheus \
prometheus2 \
alertmanager \
elasticsearch_exporter \
blackbox_exporter \
consul_exporter \
graphite_exporter \
jmx_exporter \
snmp_exporter \
apache_exporter \
collectd_exporter \
rabbitmq_exporter \
pushgateway \
sachet \
statsd_exporter \
ping_exporter 

.PHONY: $(PACKAGES7)

AUTO_GENERATED = node_exporter \
mysqld_exporter \
redis_exporter \
haproxy_exporter \
postgres_exporter \
kafka_exporter \
nginx_exporter

.PHONY: $(PACKAGES7)
.PHONY: $(AUTO_GENERATED)

all: auto $(PACKAGES7)

7: $(PACKAGES7)
auto: $(AUTO_GENERATED)


$(AUTO_GENERATED):
	python3 ./generate.py --templates $@
	# Build for centos 6
	docker run -it --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist6:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist6:/rpmbuild/RPMS/noarch \
		quay.io/zoonage/centos6-rpm-build \
		build-spec SOURCES/autogen_$@.spec
	# Test the install
	docker run -it --rm \
		-v ${PWD}/_dist6:/var/tmp/ \
		quay.io/zoonage/centos6-rpm-build \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/$@*.rpm'
	# Build for centos 7
	docker run -it --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		quay.io/zoonage/centos7-rpm-build \
		build-spec SOURCES/autogen_$@.spec
	# Test the install
	docker run --privileged -it --rm \
		-v ${PWD}/_dist7:/var/tmp/ \
		quay.io/zoonage/centos7-rpm-build \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/$@*.rpm'

$(PACKAGES7):
	docker run --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		lest/centos7-rpm-builder \
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
		quay.io/zoonage/centos7-rpm-build \
		bin/sign

publish: sign
	package_cloud push --skip-errors prometheus-rpm/release/el/7 _dist7/*.rpm
	package_cloud push --skip-errors prometheus-rpm/release/el/6 _dist6/*.rpm

clean:
	rm -rf _dist*
	rm -f **/*.tar.gz
	rm -f **/*.jar
