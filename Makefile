.PHONY: clean build test publish test-publish install

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python3 -m pip install --upgrade build
	python3 -m build

install:
	pip install -e .

test: clean build
	python3 -m pip install dist/cdek_sdk_2-*.whl --force-reinstall
	python3 -c "import cdek; print(cdek.__version__)"
	python3 -c "from cdek import CdekClient; print('✓ Import successful')"

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*

check:
	twine check dist/*

