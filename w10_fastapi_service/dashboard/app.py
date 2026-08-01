import os

from dash import Dash
from dotenv import load_dotenv

from dashboard.callbacks import register_callbacks
from dashboard.layout import create_layout

load_dotenv()

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
        debug=os.getenv("DASH_DEBUG", "True").lower() == "true",
        host="0.0.0.0",
        port=8051,
    )