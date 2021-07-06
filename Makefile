# Only run install if requirements.txt is newer than SITE_PACKAGES location
.PHONY: install
SITE_PACKAGES := $(shell pip show pip | grep '^Location' | cut -f2 -d':')
install: $(SITE_PACKAGES)

$(SITE_PACKAGES): requirements.txt
	python -m pip freeze > requirements.txt

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
