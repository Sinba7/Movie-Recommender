echo 'istart nstalling required packages'
pip install -r requirements.txt
echo 'successfully installed required packages'
echo 'start the movie recommendation app'
python src/dash_app.py