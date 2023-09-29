(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

poetry update
poetry run python ./main.py