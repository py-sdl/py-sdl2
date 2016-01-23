PYTHON ?= python
top_srcdir := `pwd`
PYTHONPATH ?= $(top_srcdir)
SUBDIRS = \
	$(top_srcdir)/sdl2 \
	$(top_srcdir)/sdl2/ext \
	$(top_srcdir)/sdl2/test \
	$(top_srcdir)/sdl2/test/resources \
	$(top_srcdir)/sdl2/test/util \
	$(top_srcdir)/doc \
	$(top_srcdir)/doc/tutorial \
	$(top_srcdir)/doc/modules \
	$(top_srcdir)/examples

INTERPRETERS = python2.7 python3.2 python3.3 python3.4 python3.5 pypy

all: clean build

dist: clean docs
	@echo "Creating dist..."
	@$(PYTHON) setup.py sdist --format gztar
	@$(PYTHON) setup.py sdist --format zip

bdist: clean docs
	@echo "Creating bdist..."
	@$(PYTHON) setup.py bdist

build:
	@echo "Running build"
	@$(PYTHON) setup.py build
	@echo "Build finished, invoke 'make install' to install."


install:
	@echo "Installing..."
	@$(PYTHON) setup.py install

clean:
	@echo "Cleaning up in $(top_srcdir)/ ..."
	@rm -f *.cache *.core *~ MANIFEST *.pyc *.orig *.rej
	@rm -rf __pycache__
	@rm -rf build dist doc/html

	@for dir in $(SUBDIRS); do \
		echo "Cleaning up in $$dir ..."; \
		if test -f $$dir/Makefile; then \
			make -C $$dir clean; \
		fi; \
		cd $$dir && rm -f *.cache *.core *~ MANIFEST *.pyc *.orig *.rej; \
	done

docs:
	@echo "Creating docs package"
	@rm -rf doc/html
	@cd doc && PYTHONPATH=$(PYTHONPATH) make html
	@mv doc/_build/html doc/html
	@rm -rf doc/_build
	@cd doc && make clean

release: dist

runtest:
	@PYTHONPATH=$(PYTHONPATH) $(PYTHON) -B -m sdl2.test.util.runtests

testall:
	@for interp in $(INTERPRETERS); do \
		PYTHONPATH=$(PYTHONPATH) $$interp -B -m sdl2.test.util.runtests || true; \
	done

# Do not run these in production environments! They are for testing
# purposes only!

buildall: clean
	@for interp in $(INTERPRETERS); do \
		$$interp setup.py build; \
	done

installall:
	@for interp in $(INTERPRETERS); do \
		$$interp setup.py install; \
	done

testpackage:
	@for interp in $(INTERPRETERS); do \
		$$interp -c "import sdl2.test; sdl2.test.run()" || true \
	done

purge_installs:
	@for interp in $(INTERPRETERS); do \
		rm -rf /usr/local/lib/$$interp/site-packages/sdl2*; \
	done
