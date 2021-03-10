# opencv	 
version = 4.1.0
release = 1
name = opencv
full_name = $(name)-$(version)
full_contrib_name = $(name)-contrib-$(version)
download_url = "https://github.com/$(name)/$(name)/archive/$(version).tar.gz"
download_contrib_url = "https://github.com/$(name)/opencv_contrib/archive/$(version).tar.gz"

all: rpm

clean:
	rm -rf rpmbuild

mkdir: clean
	mkdir -p rpmbuild
	mkdir -p rpmbuild/BUILD
	mkdir -p rpmbuild/BUILDROOT
	mkdir -p rpmbuild/RPMS
	mkdir -p rpmbuild/SOURCES
	mkdir -p rpmbuild/SRPMS

download: mkdir
	curl -L -o rpmbuild/SOURCES/$(full_name).tar.gz $(download_url); 
	curl -L -o rpmbuild/SOURCES/$(full_contrib_name).tar.gz $(download_contrib_url); 

rpm: download
	rpmbuild $(RPM_OPTS) \
	  --define "_topdir %(pwd)" \
	  --define "_builddir %{_topdir}/rpmbuild/BUILD" \
	  --define "_buildrootdir %{_topdir}/rpmbuild/BUILDROOT" \
	  --define "_rpmdir %{_topdir}/rpmbuild/RPMS" \
	  --define "_srcrpmdir %{_topdir}/rpmbuild/SRPMS" \
	  --define "_specdir %{_topdir}" \
	  --define "_sourcedir %{_topdir}/rpmbuild/SOURCES" \
	  --define "VERSION $(version)" \
 	  --define "RELEASE $(release)" \
	  -ba $(name).spec
