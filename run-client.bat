python -m venv env
CALL env\Scripts\activate.bat
pip install -r requirements.txt
python -m client.__init__
deactivate