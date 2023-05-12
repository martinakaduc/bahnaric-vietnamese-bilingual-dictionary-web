export SCRIPT_NAME=/bahnar/bilingual-dictionary
gunicorn --config gunicorn-cfg.py main:app
