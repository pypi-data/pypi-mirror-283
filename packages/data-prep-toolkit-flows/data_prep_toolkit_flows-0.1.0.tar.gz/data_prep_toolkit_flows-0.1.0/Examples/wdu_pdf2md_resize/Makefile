# Use make help, to see the available rules
REPOROOT=../../../../

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

DIRS := transforms/universal/wdu_pdf2md transforms/universal/resize 

build:: build-dist 

#build:: update-toml .defaults.build-dist 
build-dist :: set-versions .defaults.build-dist 

publish:: publish-dist 

publish-dist :: .check-env .defaults.publish-dist 

venv::  
	$(MAKE) ${VENV}/bin/activate .defaults.install-local-requirements-venv
	. ${VENV}/bin/activate && pip install "kfp==2.8.0"
	. ${VENV}/bin/activate && pip install jupyter
	. ${VENV}/bin/activate && pip install ipykernel
	for dir in $(DIRS); do \
		echo  ${REPOROOT}/$$dir; \
		if [ -e "${REPOROOT}/$$dir/python" ] && [ ! -e "$$dir/ray" ] ; then \
			$(MAKE) VENV=${CURDIR}/venv -C ${REPOROOT}/$$dir/python venv;       \
		fi;	\
		if [ -e "${REPOROOT}/$$dir/ray" ]; then 				\
			$(MAKE) VENV=${CURDIR}/venv -C ${REPOROOT}/$$dir/ray venv;      \
		fi	\
	done
	. ${VENV}/bin/activate && pip install -e ${REPOROOT}/data-processing-lib/flows

image:: 
	@# Help: Placeholder does nothing for now.
	@echo "Image building for ray is in the works (comming soon)."


run:
	. ${VENV}/bin/activate && python local_subprocess_wdu_resize_super_pipeline.py
# Here we run each test directory of tests and each ray launched test separately, because
# it seems when running multiple ray launch tests in a single pytest run there is some sort of ray.init() duplication.
# pytest-forked was tried, but then we get SIGABRT in pytest when running the s3 tests, some of which are skipped.. 
# TODO: the following fails.  Why?  source venv/bin/activate; export PYTHONPATH=../src; cd test; $(PYTEST)  .

run_jupyter:
	  . ${VENV}/bin/activate && python -m ipykernel install --user --name=venv --display-name="Python venv"
	  . ${VENV}/bin/activate && jupyter notebook
test::


