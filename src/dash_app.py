from flask import Flask
import dash
from stylesheets import *
from layout_functions import get_layout
from callbacks import register_callbacks

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    # requests_pathname_prefix = 
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts
)

app.config['suppress_callback_exceptions']=True

app.layout = get_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)