PACKAGES = prometheus \
alertmanager \
node_exporter \
mysqld_exporter \
blackbox_exporter

.PHONY: $(PACKAGES)

all: $(PACKAGES)

$(PACKAGES):
	docker run --rm \
		-v ${PWD}/$@:/rpmbuild/SOURCES \
		-v ${PWD}/_dist:/rpmbuild/RPMS/x86_64 \
		lest/centos7-rpm-builder \
		build-spec SOURCES/$@.spec

publish:
	package_cloud push --skip-errors prometheus-rpm/release/el/7 _dist/*.rpm

clean:
	rm -rf _dist
	rm **/*.tar.gz
