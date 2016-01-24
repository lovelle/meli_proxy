build:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

clean:
	rm -rf .Python build dist venv* *.egg-info *.egg
	rm -rf .Python build dist *.egg-info *.egg
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: build test clean
