# Download and install Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org/ -UseBasicParsing).Content | py -

# Add Path to PowerShell Profile
Add-Content $PROFILE -Value 'Set-Variable -Name PATH -Value "%APPDATA%\pypoetry\venv\Scripts;$PATH"'

# Update Poetry Dependencies
& (Join-Path $env:APPDATA "pypoetry\venv\Scripts\poetry") update

# Run Python Script with Poetry
& (Join-Path $env:APPDATA "pypoetry\venv\Scripts\poetry") run python ./main.py
