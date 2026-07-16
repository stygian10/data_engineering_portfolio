from dash import Dash

from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks


app = Dash(__name__)

app.title = "Prediction Analytics Dashboard"

app.layout = create_layout()

register_callbacks(app)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8051,
        debug=True,
    )