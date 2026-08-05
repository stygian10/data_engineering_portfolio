from dash import Dash

from .config import (
    W6_DASH_HOST,
    W6_DASH_PORT,
    W6_DASH_DEBUG,
)
from .dashboard import (
    app_layout,
    register_callbacks,
)

app = Dash(__name__)

app.title = "Weather Intelligence Dashboard"

app.layout = app_layout

register_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(
    host=W6_DASH_HOST,
    port=W6_DASH_PORT,
    debug=W6_DASH_DEBUG,
    )