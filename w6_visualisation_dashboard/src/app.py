from dash import Dash, html, dcc, Output, Input
import pandas as pd
import boto3
from io import BytesIO
import plotly.express as px
import logging

logging.basicConfig(level=logging.INFO)

# ----------------------------
# MinIO Configuration
# ----------------------------
MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "weather-data-lake"
PREFIX = "processed/weather/"

# ----------------------------
# Load Parquet from MinIO
# ----------------------------
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

resp = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
keys = [o["Key"] for o in resp.get("Contents", []) if o["Key"].endswith(".parquet")]

dfs = []
for k in keys:
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=k)
    dfs.append(pd.read_parquet(BytesIO(obj["Body"].read())))

if dfs:
    df = pd.concat(dfs, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
else:
    logging.warning("No Parquet data found in MinIO bucket.")
    df = pd.DataFrame(columns=[
        "city", "date", "avg_temp", "max_temp", "min_temp",
        "avg_humidity", "avg_windspeed", "rolling_avg_temp"
    ])

# ----------------------------
# Styling
# ----------------------------
COLORS = {
    "bg": "#f4f7fb",
    "card": "#ffffff",
    "text": "#1f2c3d",
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
# App Initialization
# ----------------------------
app = Dash(__name__)
app.title = "Weather Dashboard - Week 6"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(
    [
        html.H1("Weather Analytics Dashboard", style={"color": COLORS["text"]}),

        # Filters
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
                    style={"flex": "1"},
                ),
                html.Div(
                    [
                        html.Label("Date Range"),
                        dcc.DatePickerRange(
                            id="date-picker",
                            min_date_allowed=df["date"].min() if not df.empty else None,
                            max_date_allowed=df["date"].max() if not df.empty else None,
                            start_date=df["date"].min() if not df.empty else None,
                            end_date=df["date"].max() if not df.empty else None,
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

        # Charts
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
    style={"padding": "20px", "backgroundColor": COLORS["bg"]},
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
    [Input("city-dropdown", "value"), Input("date-picker", "start_date"), Input("date-picker", "end_date")],
)
def update_dashboard(cities, start_date, end_date):

    if df.empty or not cities:
        empty_fig = px.line()
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, "N/A", "N/A", "N/A", "0"

    dff = df[
        (df["city"].isin(cities)) &
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ]

    # KPIs (safe)
    avg_temp = f"{dff['avg_temp'].mean():.1f}°C" if not dff.empty else "N/A"
    avg_humidity = f"{dff['avg_humidity'].mean():.1f}%" if not dff.empty else "N/A"
    avg_wind = f"{dff['avg_windspeed'].mean():.1f}" if not dff.empty else "N/A"
    record_count = str(len(dff))

    # Charts
    avg_fig = px.line(dff, x="date", y="avg_temp", color="city", template="plotly_white", title="Avg Temperature")
    roll_fig = px.line(dff, x="date", y="rolling_avg_temp", color="city", template="plotly_white", title="7-Day Rolling Avg Temp")
    hum_fig = px.line(dff, x="date", y="avg_humidity", color="city", template="plotly_white", title="Humidity")
    wind_fig = px.line(dff, x="date", y="avg_windspeed", color="city", template="plotly_white", title="Wind Speed")

    # Min-Max Fix (melt)
    minmax_df = dff.melt(
        id_vars=["date", "city"],
        value_vars=["min_temp", "max_temp"],
        var_name="metric",
        value_name="temp"
    )
    minmax_fig = px.line(
        minmax_df,
        x="date",
        y="temp",
        color="city",
        line_dash="metric",
        template="plotly_white",
        title="Min vs Max Temperature"
    )

    return avg_fig, roll_fig, hum_fig, wind_fig, minmax_fig, avg_temp, avg_humidity, avg_wind, record_count


# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)