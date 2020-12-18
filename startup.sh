echo 'start installing required packages'
pip install -r requirements.txt
echo 'successfully installed required packages'
echo 'starting the movie recommendation app'
gunicorn src.dash_app:app_server