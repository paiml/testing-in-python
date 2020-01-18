setup:
	#create virtualenv python3 -m venv ~/.tip
	#activate virtualenv: source ~/.tip/bin/activate

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=chapter4 tests/*.py
	#python -m pytest --nbval notebook.ipynb

lint:
	pylint --disable=R,C chapter4/*.py

all: install lint test