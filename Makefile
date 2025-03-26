MANUAL = prometheus2 \
thanos \
jmx_exporter \
rabbitmq_exporter \
ping_exporter \
couchbase_exporter \
mtail \

AUTO_GENERATED = alertmanager \
node_exporter \
blackbox_exporter \
snmp_exporter \
pushgateway \
mysqld_exporter \
elasticsearch_exporter \
postgres_exporter \
pgbouncer_exporter \
redis_exporter \
haproxy_exporter \
kafka_exporter \
nginx_exporter \
bind_exporter \
json_exporter \
keepalived_exporter \
jolokia_exporter \
frr_exporter \
domain_exporter \
mongodb_exporter \
graphite_exporter \
statsd_exporter \
collectd_exporter \
memcached_exporter \
consul_exporter \
smokeping_prober \
iperf3_exporter \
apache_exporter \
influxdb_exporter \
exporter_exporter \
junos_exporter \
openstack_exporter \
process_exporter \
ssl_exporter \
sachet \
jiralert \
ebpf_exporter \
karma \
bareos_exporter \
artifactory_exporter \
phpfpm_exporter \
ipmi_exporter \
sql_exporter \
nats_exporter \
prometheus_msteams \
cadvisor \
squid_exporter \
dellhw_exporter \
exim_exporter \
systemd_exporter \
logstash_exporter

.PHONY: $(MANUAL) $(AUTO_GENERATED)

INTERACTIVE:=$(shell [ -t 0 ] && echo 1)
ifdef INTERACTIVE
	DOCKER_FLAGS = -it --rm
else
	DOCKER_FLAGS = --rm
endif

all: auto manual

manual: $(MANUAL)
auto: $(AUTO_GENERATED)

manual9: $(addprefix build9-,$(MANUAL))
manual8: $(addprefix build8-,$(MANUAL))
manual7: $(addprefix build7-,$(MANUAL))

$(addprefix build9-,$(MANUAL)):
	$(eval PACKAGE=$(subst build9-,,$@))
	[ -d ${PWD}/_dist9 ] || mkdir ${PWD}/_dist9 
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf 
	docker run ${DOCKER_FLAGS} \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist9:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist9:/rpmbuild/RPMS/noarch \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle9 \
		build-spec SOURCES/${PACKAGE}.spec
	# Test the install
	[ -d ${PWD}/_dist9 ] || mkdir ${PWD}/_dist9      
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf
	docker run --privileged ${DOCKER_FLAGS} \
		-v ${PWD}/_dist9:/var/tmp/ \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle9 \
		/bin/bash -c '/usr/bin/dnf install --verbose -y /var/tmp/${PACKAGE}*.rpm'

$(addprefix build8-,$(MANUAL)):
	$(eval PACKAGE=$(subst build8-,,$@))
	[ -d ${PWD}/_dist8 ] || mkdir ${PWD}/_dist8 
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf 
	docker run ${DOCKER_FLAGS} \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/noarch \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle8 \
		build-spec SOURCES/${PACKAGE}.spec
	# Test the install
	[ -d ${PWD}/_dist8 ] || mkdir ${PWD}/_dist8      
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf
	docker run --privileged ${DOCKER_FLAGS} \
		-v ${PWD}/_dist8:/var/tmp/ \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle8 \
		/bin/bash -c '/usr/bin/dnf install --verbose -y /var/tmp/${PACKAGE}*.rpm'

$(addprefix build7-,$(MANUAL)):
	$(eval PACKAGE=$(subst build7-,,$@))
	[ -d ${PWD}/_dist7 ] || mkdir ${PWD}/_dist7      
	[ -d ${PWD}/_cache_yum ] || mkdir ${PWD}/_cache_yum
	docker run ${DOCKER_FLAGS} \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		-v ${PWD}/_cache_yum:/var/cache/yum \
		ghcr.io/lest/centos-rpm-builder:7 \
		build-spec SOURCES/${PACKAGE}.spec
	# Test the install
	[ -d ${PWD}/_dist7 ] || mkdir ${PWD}/_dist7      
	[ -d ${PWD}/_cache_yum ] || mkdir ${PWD}/_cache_yum
	docker run --privileged ${DOCKER_FLAGS} \
		-v ${PWD}/_dist7:/var/tmp/ \
		-v ${PWD}/_cache_yum:/var/cache/yum \
		ghcr.io/lest/centos-rpm-builder:7 \
		/bin/bash -c '/usr/bin/yum install --verbose -y /var/tmp/${PACKAGE}*.rpm'


auto9: $(addprefix build9-,$(AUTO_GENERATED))
auto8: $(addprefix build8-,$(AUTO_GENERATED))
auto7: $(addprefix build7-,$(AUTO_GENERATED))

$(addprefix build9-,$(AUTO_GENERATED)):
	$(eval PACKAGE=$(subst build9-,,$@))

	python3 ./generate.py --templates ${PACKAGE}
	[ -d ${PWD}/_dist9 ] || mkdir ${PWD}/_dist9      
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf
	docker run ${DOCKER_FLAGS} \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist9:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist9:/rpmbuild/RPMS/noarch \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle9 \
		build-spec SOURCES/autogen_${PACKAGE}.spec
	# Test the install
	[ -d ${PWD}/_dist9 ] || mkdir ${PWD}/_dist9      
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf
	docker run --privileged ${DOCKER_FLAGS} \
		-v ${PWD}/_dist9:/var/tmp/ \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle9 \
		/bin/bash -c '/usr/bin/dnf install --verbose -y /var/tmp/${PACKAGE}*.rpm'

sign9:
	docker run --rm \
		-v ${PWD}/_dist9:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/bin:/rpmbuild/bin \
		-v ${PWD}/RPM-GPG-KEY-prometheus-rpm:/rpmbuild/RPM-GPG-KEY-prometheus-rpm \
		-v ${PWD}/secret.asc:/rpmbuild/secret.asc \
		-v ${PWD}/.passphrase:/rpmbuild/.passphrase \
		ghcr.io/lest/centos-rpm-builder:oracle9 \
		bin/sign

$(addprefix build8-,$(AUTO_GENERATED)):
	$(eval PACKAGE=$(subst build8-,,$@))

	python3 ./generate.py --templates ${PACKAGE}
	[ -d ${PWD}/_dist8 ] || mkdir ${PWD}/_dist8      
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf
	docker run ${DOCKER_FLAGS} \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/noarch \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle8 \
		build-spec SOURCES/autogen_${PACKAGE}.spec
	# Test the install
	[ -d ${PWD}/_dist8 ] || mkdir ${PWD}/_dist8      
	[ -d ${PWD}/_cache_dnf ] || mkdir ${PWD}/_cache_dnf
	docker run --privileged ${DOCKER_FLAGS} \
		-v ${PWD}/_dist8:/var/tmp/ \
		-v ${PWD}/_cache_dnf:/var/cache/dnf \
		ghcr.io/lest/centos-rpm-builder:oracle8 \
		/bin/bash -c '/usr/bin/dnf install --verbose -y /var/tmp/${PACKAGE}*.rpm'

sign8:
	docker run --rm \
		-v ${PWD}/_dist8:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/bin:/rpmbuild/bin \
		-v ${PWD}/RPM-GPG-KEY-prometheus-rpm:/rpmbuild/RPM-GPG-KEY-prometheus-rpm \
		-v ${PWD}/secret.asc:/rpmbuild/secret.asc \
		-v ${PWD}/.passphrase:/rpmbuild/.passphrase \
		ghcr.io/lest/centos-rpm-builder:oracle8 \
		bin/sign

$(addprefix build7-,$(AUTO_GENERATED)):
	$(eval PACKAGE=$(subst build7-,,$@))

	python3 ./generate.py --templates ${PACKAGE}
	[ -d ${PWD}/_dist7 ] || mkdir ${PWD}/_dist7
	[ -d ${PWD}/_cache_yum ] || mkdir ${PWD}/_cache_yum
	docker run ${DOCKER_FLAGS} \
		-v ${PWD}/${PACKAGE}:/rpmbuild/SOURCES \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/x86_64 \
		-v ${PWD}/_dist7:/rpmbuild/RPMS/noarch \
		-v ${PWD}/_cache_yum:/var/cache/yum \
		ghcr.io/lest/centos-rpm-builder:7 \
		build-spec SOURCES/autogen_${PACKAGE}.spec
	# Test the install
	[ -d ${PWD}/_dist7 ] || mkdir ${PWD}/_dist7
	[ -d ${PWD}/_cache_yum ] || mkdir ${PWD}/_cache_yum
	docker run --privileged ${DOCKER_FLAGS} \
		-v ${PWD}/_dist7:/var/tmp/ \
		-v ${PWD}/_cache_yum:/var/cache/yum \
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
			$(addprefix build9-,${PACKAGE}) \
			$(addprefix build8-,${PACKAGE}) \
			$(addprefix build7-,${PACKAGE}) \
	) \
)

$(foreach \
	PACKAGE,$(AUTO_GENERATED),$(eval \
		${PACKAGE}: \
			$(addprefix build9-,${PACKAGE}) \
			$(addprefix build8-,${PACKAGE}) \
			$(addprefix build7-,${PACKAGE}) \
	) \
)

sign: sign9 sign8 sign7

publish9: sign9
	package_cloud push --skip-errors prometheus-rpm/release/el/9 _dist9/*.rpm

publish8: sign8
	package_cloud push --skip-errors prometheus-rpm/release/el/8 _dist8/*.rpm

publish7: sign7
	package_cloud push --skip-errors prometheus-rpm/release/el/7 _dist7/*.rpm

publish: publish9 publish8 publish7

clean:
	rm -rf _cache_dnf _cache_yum _dist*
	rm -f **/*.tar.gz
	rm -f **/*.jar
	rm -f **/autogen_*{default,init,unit,spec}
