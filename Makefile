SHELL:=/bin/bash

COURSE_PATH ?= coursebook

TERM_BOLD	:= $(shell (tput setaf 6 && tput bold) 2>/dev/null)
TERM_RESET	:= $(shell (tput sgr0) 2>/dev/null)

default: html

.PHONY: git-clean
git-clean:
	$(call echo_bold,>>> Clean git working tree)
	git clean -xdf

.PHONY: clean
clean:
	$(call echo_bold,>>> Clean the .build folder)
	jupyter-book clean $(COURSE_PATH)

.PHONY: html
html:
	$(call echo_bold,>>> Build HTML pages)
	jupyter-book build --verbose --keep-going $(COURSE_PATH)
	@echo "Copy a redirect page to the generated html content"
	cp "$(COURSE_PATH)/index.html" "$(COURSE_PATH)/_build"

.PHONY: pdf
pdf:
	$(call echo_bold,>>> Build PDF)
	jupyter-book build --builder pdfhtml --verbose --keep-going $(COURSE_PATH)
	@echo "Remove the html output"
	jupyter-book clean --html $(COURSE_PATH)

.PHONY: gh-hacks
# Add the .nojekyll directive to stop GitHub Pages excluding directories with underscores
# See https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages#static-site-generators
gh-hacks:
	$(call echo_bold,>>> Apply workaround for GitHub Pages excluded directories)
	touch $(COURSE_PATH)/_build/.nojekyll
	touch $(COURSE_PATH)/_build/html/.nojekyll

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Development

# Initializes poetry. Please be aware of the `poetry.toml` file that enforces the creation
# of a `.venv` folder inside the project's folder. This is convenient to avoid messing up
# the configuration at OS level.
# In summary, this target sets the python used by Poetry and then install all the
# dependencies (or updates them).
# Note: it is highly recommended to use a Python Version Management (such as pyenv) instead
#       of relying on the Python binary provided by your OS.
.PHONY: init
init:
	$(call echo_bold,>>> Project initialization)
	@echo "Creating the virtual environment ..."
	@poetry env use python3
	@echo "Installing project dependencies ..."
	poetry install || poetry update

.PHONY: requirements
requirements:
	$(call echo_bold,>>> Export requirement.txt file)
	@poetry export --without-hashes -o binder/requirements.txt

.PHONY: jupyter-start
jupyter-start:
	jupyter notebook --no-browser --port=8898

# echo_bold,msg
# Print a message with bold font
define echo_bold
	@echo "$(TERM_BOLD)$(1)$(TERM_RESET)"
endef
