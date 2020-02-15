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

test:
	@$(PYTHON) -B -m pytest -vvl -rxXP
