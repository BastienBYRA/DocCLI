## Créer l'environnement virtuel
- Linux : source .venv/bin/activate
- Windows CMD : .\.venv\Scripts\activate.bat
- Windows Powershell : Set-ExecutionPolicy Unrestricted -Scope Process et .\.venv\Scripts\activate.ps1

Plus d'info : https://docs.python.org/3/library/venv.html#how-venvs-work

## Quitter l'environnement virtuel
deactivate

## Lancer le projet
cd .\CLI\
uv run .\doccli\