(Invoke-WebRequest -Uri https://install.python-poetry.org/ -UseBasicParsing).Content | py -

Add-Content $PROFILE -Value 'Set-Variable -Name PATH -Value "%APPDATA%\pypoetry\venv\Scripts;$PATH"'

& (Join-Path $env:APPDATA "pypoetry\venv\Scripts\poetry") update
& (Join-Path $env:APPDATA "pypoetry\venv\Scripts\poetry") add flake8-html --group dev
& "$env:APPDATA\pypoetry\venv\Scripts\poetry" run flake8 --config=setup.cfg --format=html --htmldir=flake8_report
