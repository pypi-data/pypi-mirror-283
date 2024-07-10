# Use make help, to see the available rules
REPOROOT=../..

include $(REPOROOT)/transforms/.make.transforms

TAG := "v${DPK_LIB_VERSION}"


clean::
	@# Help: Clean up the distribution build and the venv 
	rm -rf dist venv
	rm -rf src/*egg-info

.check-env::
	@echo "Checks passed"

setup::

set-versions: .check-env
	# TODO: Should we define a separate version
	$(MAKE) TOML_VERSION=$(DPK_LIB_VERSION) .defaults.update-toml
	cat pyproject.toml | sed -e 's/"kfp\([=><][=><]\).*",/"kfp\1$(KFP_v2_SDK)",/' > tt.toml
	mv tt.toml pyproject.toml

ALL_UNIVERSAL_DIRS := $(shell find $(REPOROOT)/transforms/universal -maxdepth 1 -type d ) 

build:: build-dist 

#build:: update-toml .defaults.build-dist 
build-dist :: set-versions .defaults.build-dist 

publish:: publish-dist 

publish-dist :: .check-env .defaults.publish-dist 

venv::  
	$(MAKE) ${VENV}/bin/activate .defaults.install-local-requirements-venv
	for dir in ${ALL_UNIVERSAL_DIRS}; do \
		if [ -e "$$dir/python" ] && [ ! -e "$$dir/ray" ] ; then \
			$(MAKE) VENV=${CURDIR}/venv -C $$dir/python venv;       \
		fi;	\
		if [ -e "$$dir/ray" ]; then 				\
			$(MAKE) VENV=${CURDIR}/venv -C $$dir/ray venv;      \
		fi	\
	done

image:: 
	@# Help: Placeholder does nothing for now.
	@echo "Image building for ray is in the works (comming soon)."

# Here we run each test directory of tests and each ray launched test separately, because
# it seems when running multiple ray launch tests in a single pytest run there is some sort of ray.init() duplication.
# pytest-forked was tried, but then we get SIGABRT in pytest when running the s3 tests, some of which are skipped.. 
# TODO: the following fails.  Why?  source venv/bin/activate; export PYTHONPATH=../src; cd test; $(PYTEST)  . 
test::


