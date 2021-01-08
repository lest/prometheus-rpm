MANUAL = prometheus2 \
alertmanager \
thanos \
elasticsearch_exporter \
blackbox_exporter \
consul_exporter \
jmx_exporter \
snmp_exporter \
apache_exporter \
collectd_exporter \
rabbitmq_exporter \
sachet \
statsd_exporter \
ping_exporter \
postgres_exporter \
process_exporter \
memcached_exporter \
smokeping_prober \
exporter_exporter \
iperf3_exporter \
couchbase_exporter \
junos_exporter \
ssl_exporter \
mtail \
openstack_exporter \
jiralert

AUTO_GENERATED = node_exporter \
pushgateway \
mysqld_exporter \
redis_exporter \
haproxy_exporter \
kafka_exporter \
nginx_exporter \
bind_exporter \
keepalived_exporter \
jolokia_exporter \
frr_exporter \
domain_exporter \
mongodb_exporter \
graphite_exporter

.PHONY: $(MANUAL) $(AUTO_GENERATED)

all: auto manual

manual: $(MANUAL)
auto: $(AUTO_GENERATED)

manual8: $(addprefix build8-,$(MANUAL))
manual7: $(addprefix build7-,$(MANUAL))

$(addprefix build8-,$(MANUAL)):
	$(eval PACKAGE=$(subst build8-,,$@))
	docker run -it --rm \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/noarch \
		ghcr.io/lest/centos-rpm-builder:8 \
		build-spec SOURCES/${PACKAGE}.spec
	# Test the install
	docker run --privileged -it --rm \
		-v ${PWD}/_dist8:/var/tmp/ \
		ghcr.io/lest/centos-rpm-builder:8 \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/${PACKAGE}*.rpm'

$(addprefix build7-,$(MANUAL)):
	$(eval PACKAGE=$(subst build7-,,$@))
	docker run -it --rm \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		ghcr.io/lest/centos-rpm-builder:7 \
		build-spec SOURCES/${PACKAGE}.spec
	# Test the install
	docker run --privileged -it --rm \
		-v ${PWD}/_dist7:/var/tmp/ \
		ghcr.io/lest/centos-rpm-builder:7 \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/${PACKAGE}*.rpm'


auto8: $(addprefix build8-,$(AUTO_GENERATED))
auto7: $(addprefix build7-,$(AUTO_GENERATED))

$(addprefix build8-,$(AUTO_GENERATED)):
	$(eval PACKAGE=$(subst build8-,,$@))

	python3 ./generate.py --templates ${PACKAGE}

	docker run -it --rm \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/noarch \
		ghcr.io/lest/centos-rpm-builder:8 \
		build-spec SOURCES/autogen_${PACKAGE}.spec
	# Test the install
	docker run --privileged -it --rm \
		-v ${PWD}/_dist8:/var/tmp/ \
		ghcr.io/lest/centos-rpm-builder:8 \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/${PACKAGE}*.rpm'

sign8:
	docker run --rm \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/bin:/rpmbuild/bin \
		-v ${PWD}/RPM-GPG-KEY-prometheus-rpm:/rpmbuild/RPM-GPG-KEY-prometheus-rpm \
		-v ${PWD}/secret.asc:/rpmbuild/secret.asc \
		-v ${PWD}/.passphrase:/rpmbuild/.passphrase \
		ghcr.io/lest/centos-rpm-builder:8 \
		bin/sign

$(addprefix build7-,$(AUTO_GENERATED)):
	$(eval PACKAGE=$(subst build7-,,$@))

	python3 ./generate.py --templates ${PACKAGE}

	docker run -it --rm \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		ghcr.io/lest/centos-rpm-builder:7 \
		build-spec SOURCES/autogen_${PACKAGE}.spec
	# Test the install
	docker run --privileged -it --rm \
		-v ${PWD}/_dist7:/var/tmp/ \
		ghcr.io/lest/centos-rpm-builder:7 \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/${PACKAGE}*.rpm'

sign7:
	docker run --rm \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/bin:/rpmbuild/bin \
		-v ${PWD}/RPM-GPG-KEY-prometheus-rpm:/rpmbuild/RPM-GPG-KEY-prometheus-rpm \
		-v ${PWD}/secret.asc:/rpmbuild/secret.asc \
		-v ${PWD}/.passphrase:/rpmbuild/.passphrase \
		ghcr.io/lest/centos-rpm-builder:7 \
		bin/sign

$(foreach \
	PACKAGE,$(MANUAL),$(eval \
		${PACKAGE}: \
			$(addprefix build8-,${PACKAGE}) \
			$(addprefix build7-,${PACKAGE}) \
	) \
)

$(foreach \
	PACKAGE,$(AUTO_GENERATED),$(eval \
		${PACKAGE}: \
			$(addprefix build8-,${PACKAGE}) \
			$(addprefix build7-,${PACKAGE}) \
	) \
)

sign: sign8 sign7

publish8: sign8
	package_cloud push --skip-errors prometheus-rpm/release/el/8 _dist8/*.rpm

publish7: sign7
	package_cloud push --skip-errors prometheus-rpm/release/el/7 _dist7/*.rpm

publish: publish8 publish7

clean:
	rm -rf _dist*
	rm -f **/*.tar.gz
	rm -f **/*.jar
	rm -f **/autogen_*{init,unit,spec}
