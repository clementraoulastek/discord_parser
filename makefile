build:
	pyinstaller --onefile src/main.py --name "DofusParser"

run:
	python -m src

lint:
	python -m isort . --profile black
	python -m black .
	python -m pylint src --disable=line-too-long --disable=anomalous-backslash-in-string