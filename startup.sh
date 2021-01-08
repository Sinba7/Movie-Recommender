echo 'Start installing required packages'
pip install -r requirements.txt
echo 'Successfully installed required packages'

echo 'Start testing'
pytest --cov-report term-missing --cov='src'
echo 'Pass all tests'

echo 'Initializing the movie recommendation app'
gunicorn src.dash_app:app_server