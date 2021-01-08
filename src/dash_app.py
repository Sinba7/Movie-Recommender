from flask import Flask
import dash
# from src.layout_functions import get_layout
# from src.callbacks import register_callbacks
from src.stylesheets import *
from src.callbacks import register_callbacks, get_layout

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    # requests_pathname_prefix =
    meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts
)

app_server = app.server
app.config['suppress_callback_exceptions']=True

app.layout = get_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)