build:
	python3 -m build

dev:
	python3 -m venv venv
	venv/bin/python3 -m pip install --upgrade pip
	venv/bin/pip install -e .
	venv/bin/pip install .[dev]

clean:
	rm -rf dist/
	rm -rf *.egg-info/
