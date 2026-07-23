from dash import Dash

from dashboard.callbacks import register_callbacks
from dashboard.layout import create_layout


# Create Dash application

app = Dash(
    __name__,
    title="Weather Prediction Dashboard",
)


# Dashboard layout

app.layout = create_layout()


# Register callbacks

register_callbacks(app)


# Server instance (for deployment)

server = app.server


# Run dashboard

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=8051,
    )