PACKAGES = prometheus alertmanager node_exporter mysqld_exporter

.PHONY: $(PACKAGES)

all: $(PACKAGES)

$(PACKAGES):
	docker run --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist:/rpmbuild/RPMS/x86_64 \
		lest/centos7-rpm-builder \
		build-spec SOURCES/$@.spec

clean:
	rm -rf _dist
	rm **/*.tar.gz
