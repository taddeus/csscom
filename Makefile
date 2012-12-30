TEST_OPTIONS := --failfast --catch
COVERAGE_OPTIONS := --branch
COVERAGE_DIR := coverage

.PHONY: test coverage pyclean clean

test:
	@PYTHONDONTWRITEBYTECODE=x python -m unittest discover -s tests \
		-p 'test_*.py' $(TEST_OPTIONS)

coverage:
	@python-coverage erase
	@rm -rf $(COVERAGE_DIR)
	@PYTHONDONTWRITEBYTECODE=x PYTHONPATH=. python-coverage run --source=. \
		--omit=tests/* $(COVERAGE_OPTIONS) tests/run.py
	@python-coverage report
	@python-coverage html --directory=$(COVERAGE_DIR)

pyclean:
	find -name \*.pyc -delete

clean: pyclean
	rm -rf $(COVERAGE_DIR)
