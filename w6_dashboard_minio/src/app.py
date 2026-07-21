from dash import Dash

from dashboard import app_layout, register_callbacks

app = Dash(__name__)

app.title = "Weather Intelligence Dashboard"

app.layout = app_layout

register_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=True,
    )