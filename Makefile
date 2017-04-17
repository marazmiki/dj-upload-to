.PHONY: test release flake8 cov clean


test:
	python setup.py develop
	python setup.py test
	python setup.py develop --uninstall


release:
	python setup.py sdist --format=zip,bztar,gztar
	python setup.py bdist_wheel
	python setup.py register upload


flake8:
	flake8 --max-complexity 12 *.py


cov:
	python setup.py develop
	coverage run --rcfile=.coveragerc --include=*.py setup.py test
	coverage report --rcfile=.coveragerc
	coverage html --rcfile=.coveragerc


clean:
	python setup.py develop --uninstall
	rm -rf *.egg-info *.egg
	rm -rf htmlcov
	rm -f .coverage
	rm -rf .cache
	rm -rf build dist
	find . -name "*.pyc" -exec rm -rf {} \;
