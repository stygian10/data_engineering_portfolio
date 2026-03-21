# src/app.py

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import boto3
from io import BytesIO
import plotly.express as px

# ----------------------------
# MinIO configuration
# ----------------------------
MINIO_ENDPOINT = "127.0.0.1:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "weather-data-lake"
PREFIX = "processed/weather/"

# ----------------------------
# Load Parquet from MinIO
# ----------------------------
s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

resp = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
keys = [o["Key"] for o in resp.get("Contents", []) if o["Key"].endswith(".parquet")]

dfs = []
for k in keys:
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=k)
    dfs.append(pd.read_parquet(BytesIO(obj["Body"].read())))

df = pd.concat(dfs, ignore_index=True)
df["date"] = pd.to_datetime(df["date"])

# ----------------------------
# Styling (centralized)
# ----------------------------
COLORS = {
    "bg": "#f4f7fb",
    "card": "#ffffff",
    "text": "#1f2c3d",
    "accent": "#2a6fdb",
    "muted": "#6b7a90",
}

CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "padding": "16px",
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "marginBottom": "16px",
}

KPI_STYLE = {
    "flex": "1",
    "minWidth": "180px",
    "marginRight": "12px",
    **CARD_STYLE,
}

# ----------------------------
# App
# ----------------------------
app = Dash(__name__)
app.title = "Weather Dashboard - Week 6"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(
    [
        # Header
        html.Div(
            [
                html.H1(
                    "Weather Analytics Dashboard",
                    style={"margin": "0", "color": COLORS["text"]},
                ),
                html.P(
                    "Spark (Week 5) → MiniO + Dash (Week 6)",
                    style={"margin": "4px 0 0 0", "color": COLORS["muted"]},
                ),
            ],
            style={"marginBottom": "20px"},
        ),

        # Filters Card
        html.Div(
            [
                html.Div(
                    [
                        html.Label("City"),
                        dcc.Dropdown(
                            id="city-dropdown",
                            options=[{"label": c, "value": c} for c in sorted(df["city"].unique())],
                            value=sorted(df["city"].unique()),
                            multi=True,
                        ),
                    ],
                    style={"flex": "1", "marginRight": "12px"},
                ),
                html.Div(
                    [
                        html.Label("Date Range"),
                        dcc.DatePickerRange(
                            id="date-picker",
                            min_date_allowed=df["date"].min(),
                            max_date_allowed=df["date"].max(),
                            start_date=df["date"].min(),
                            end_date=df["date"].max(),
                        ),
                    ],
                    style={"flex": "1"},
                ),
            ],
            style={**CARD_STYLE, "display": "flex", "gap": "12px"},
        ),

        # KPI Row
        html.Div(
            [
                html.Div([html.H4("Avg Temp"), html.H2(id="kpi-avg-temp")], style=KPI_STYLE),
                html.Div([html.H4("Avg Humidity"), html.H2(id="kpi-humidity")], style=KPI_STYLE),
                html.Div([html.H4("Avg Wind"), html.H2(id="kpi-wind")], style=KPI_STYLE),
                html.Div([html.H4("Records"), html.H2(id="kpi-count")], style=KPI_STYLE),
            ],
            style={"display": "flex", "flexWrap": "wrap"},
        ),

        # Charts Grid
        html.Div(
            [
                html.Div([dcc.Graph(id="avg-temp-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),
                html.Div([dcc.Graph(id="rolling-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),
                html.Div([dcc.Graph(id="humidity-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),
                html.Div([dcc.Graph(id="wind-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),
                html.Div([dcc.Graph(id="minmax-chart")], style={"flex": "1", "minWidth": "100%", **CARD_STYLE}),
            ],
            style={"display": "flex", "flexWrap": "wrap", "gap": "16px"},
        ),
    ],
    style={
        "padding": "20px",
        "backgroundColor": COLORS["bg"],
        "fontFamily": "Arial, sans-serif",
    },
)

# ----------------------------
# Callback
# ----------------------------
@app.callback(
    [
        Output("avg-temp-chart", "figure"),
        Output("rolling-chart", "figure"),
        Output("humidity-chart", "figure"),
        Output("wind-chart", "figure"),
        Output("minmax-chart", "figure"),
        Output("kpi-avg-temp", "children"),
        Output("kpi-humidity", "children"),
        Output("kpi-wind", "children"),
        Output("kpi-count", "children"),
    ],
    [
        Input("city-dropdown", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
    ],
)
def update_dashboard(cities, start_date, end_date):
    dff = df[
        (df["city"].isin(cities))
        & (df["date"] >= pd.to_datetime(start_date))
        & (df["date"] <= pd.to_datetime(end_date))
    ]

    # Charts
    avg_fig = px.line(dff, x="date", y="avg_temp", color="city", template="plotly_white")
    roll_fig = px.line(dff, x="date", y="rolling_avg_temp", color="city", template="plotly_white")
    hum_fig = px.line(dff, x="date", y="avg_humidity", color="city", template="plotly_white")
    wind_fig = px.line(dff, x="date", y="avg_windspeed", color="city", template="plotly_white")
    minmax_fig = px.line(dff, x="date", y=["min_temp", "max_temp"], color="city", template="plotly_white")

    # KPIs
    return (
        avg_fig,
        roll_fig,
        hum_fig,
        wind_fig,
        minmax_fig,
        f"{dff['avg_temp'].mean():.1f}°C",
        f"{dff['avg_humidity'].mean():.1f}%",
        f"{dff['avg_windspeed'].mean():.1f}",
        f"{len(dff)}",
    )

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)