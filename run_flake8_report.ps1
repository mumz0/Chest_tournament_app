if (-Not (Test-Path ./env)) {
    python -m venv env
    .\env\Scripts\activate
    pip install -r requirements.txt
} else {
    .\env\Scripts\Activate.ps1
}
flake8 --exclude=env --config=setup.cfg --format=html --htmldir=flake8_report
deactivate