
if (-Not (Test-Path ./env)) {
    python -m venv env
    .\env\Scripts\activate
    pip install -r requirements.txt
} else {
    .\env\Scripts\Activate.ps1
}

python "main.py"
deactivate
