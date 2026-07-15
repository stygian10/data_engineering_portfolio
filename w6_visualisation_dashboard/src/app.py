from dash import Dash, html, dcc, Output, Input
import pandas as pd
import boto3
from io import BytesIO
from datetime import date
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
# Connect to MinIO
# ----------------------------
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# ----------------------------
# Load Weather Dataset
# ----------------------------
response = s3.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix=PREFIX,
)

parquet_files = [
    obj["Key"]
    for obj in response.get("Contents", [])
    if obj["Key"].endswith(".parquet")
]

dataframes = []

for file in parquet_files:

    logging.info(f"Loading {file}")

    obj = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=file,
    )

    dataframe = pd.read_parquet(
        BytesIO(obj["Body"].read())
    )

    dataframes.append(dataframe)

# ----------------------------
# Combine Weather Data
# ----------------------------
if dataframes:

    df = pd.concat(
        dataframes,
        ignore_index=True,
    )

    df["date"] = pd.to_datetime(df["date"])

    logging.info(
        "Loaded %s rows from MinIO",
        len(df),
    )

else:

    logging.warning(
        "No weather data found in MinIO."
    )

    df = pd.DataFrame(
        columns=[
            "city",
            "date",
            "avg_temp",
            "max_temp",
            "min_temp",
            "avg_humidity",
            "avg_windspeed",
            "rolling_avg_temp",
        ]
    )

# ----------------------------
# App Initialization
# ----------------------------
app = Dash(__name__)

app.title = "Weather Intelligence Platform"

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
# Dashboard Layout
# ----------------------------
app.layout = html.Div(

    [

        html.H1(
            "Weather Intelligence Platform",
            style={"color": COLORS["text"]},
        ),

        # ----------------------------
        # Today's Summary
        # ----------------------------

        html.Div(

            [

                html.Div(
                    [
                        html.H4("Today's Date"),
                        html.H2(id="today-date"),
                    ],
                    style=KPI_STYLE,
                ),

                html.Div(
                    [
                        html.H4("Today's Temperature (Edinburgh)"),
                        html.H2(id="today-temp"),
                    ],
                    style=KPI_STYLE,
                ),

            ],

            style={
                "display": "flex",
                "gap": "12px",
                "marginBottom": "20px",
            },

        ),

        # ----------------------------
        # Filters
        # ----------------------------

        html.Div(

            [

                html.Div(

                    [

                        html.Label("City"),

                        dcc.Dropdown(
                            id="city-dropdown",
                            options=[
                                {"label": city, "value": city}
                                for city in sorted(df["city"].unique())
                            ],
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

            style={
                **CARD_STYLE,
                "display": "flex",
                "gap": "12px",
            },

        ),

        # ----------------------------
        # KPI Cards
        # ----------------------------

        html.Div(

            [

                html.Div(
                    [
                        html.H4("Avg Temp"),
                        html.H2(id="kpi-avg-temp"),
                    ],
                    style=KPI_STYLE,
                ),

                html.Div(
                    [
                        html.H4("Avg Humidity"),
                        html.H2(id="kpi-humidity"),
                    ],
                    style=KPI_STYLE,
                ),

                html.Div(
                    [
                        html.H4("Avg Wind"),
                        html.H2(id="kpi-wind"),
                    ],
                    style=KPI_STYLE,
                ),

                html.Div(
                    [
                        html.H4("Records"),
                        html.H2(id="kpi-count"),
                    ],
                    style=KPI_STYLE,
                ),

            ],

            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "12px",
            },

        ),

        # ----------------------------
        # Charts
        # ----------------------------

        html.Div(

            [

                html.Div([dcc.Graph(id="avg-temp-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),

                html.Div([dcc.Graph(id="rolling-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),

                html.Div([dcc.Graph(id="humidity-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),

                html.Div([dcc.Graph(id="wind-chart")], style={"flex": "1", "minWidth": "45%", **CARD_STYLE}),

                html.Div([dcc.Graph(id="minmax-chart")], style={"flex": "1", "minWidth": "100%", **CARD_STYLE}),

            ],

            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "16px",
            },

        ),

    ],

    style={
        "padding": "20px",
        "backgroundColor": COLORS["bg"],
    },

)
# ----------------------------
# Dashboard Callback
# ----------------------------
@app.callback(

    [

        Output("today-date", "children"),
        Output("today-temp", "children"),

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

    empty_fig = px.line()

    if df.empty or not cities:

        return (

            "N/A",
            "N/A",

            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,

            "N/A",
            "N/A",
            "N/A",
            "0",

        )

    dff = df[
        (df["city"].isin(cities))
        & (df["date"] >= pd.to_datetime(start_date))
        & (df["date"] <= pd.to_datetime(end_date))
    ]

    if dff.empty:

        return (

            "N/A",
            "N/A",

            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,

            "N/A",
            "N/A",
            "N/A",
            "0",

        )

    # ----------------------------
    # Today's Summary (Edinburgh)
    # ----------------------------

    today = date.today()

    edinburgh_df = df[df["city"] == "Edinburgh"].copy()

    edinburgh_df["date_only"] = edinburgh_df["date"].dt.date

    today_weather = edinburgh_df[
        edinburgh_df["date_only"] == today
    ]

    if not today_weather.empty:

        today_row = today_weather.iloc[0]

        today_date = today_row["date"].strftime("%d %B %Y")

        today_temp = f"{today_row['avg_temp']:.1f}°C"

    else:

        today_date = "No Data"

        today_temp = "N/A"

    # ----------------------------
    # Dashboard KPIs
    # ----------------------------

    avg_temp = f"{dff['avg_temp'].mean():.1f}°C"

    avg_humidity = f"{dff['avg_humidity'].mean():.1f}%"

    avg_wind = f"{dff['avg_windspeed'].mean():.1f}"

    record_count = str(len(dff))


    # ----------------------------
    # Charts
    # ----------------------------

    avg_fig = px.line(
        dff,
        x="date",
        y="avg_temp",
        color="city",
        template="plotly_white",
        title="Average Temperature",
    )

    roll_fig = px.line(
        dff,
        x="date",
        y="rolling_avg_temp",
        color="city",
        template="plotly_white",
        title="7-Day Rolling Average Temperature",
    )

    hum_fig = px.line(
        dff,
        x="date",
        y="avg_humidity",
        color="city",
        template="plotly_white",
        title="Average Humidity",
    )

    wind_fig = px.line(
        dff,
        x="date",
        y="avg_windspeed",
        color="city",
        template="plotly_white",
        title="Average Wind Speed",
    )

    minmax_df = dff.melt(
        id_vars=["date", "city"],
        value_vars=["min_temp", "max_temp"],
        var_name="metric",
        value_name="temperature",
    )

    minmax_fig = px.line(
        minmax_df,
        x="date",
        y="temperature",
        color="city",
        line_dash="metric",
        template="plotly_white",
        title="Minimum vs Maximum Temperature",
    )

    # ----------------------------
    # Return Dashboard Components
    # ----------------------------

    return (

        today_date,
        today_temp,

        avg_fig,
        roll_fig,
        hum_fig,
        wind_fig,
        minmax_fig,

        avg_temp,
        avg_humidity,
        avg_wind,
        record_count,

    )


# ----------------------------
# Run Dashboard
# ----------------------------
if __name__ == "__main__":

    logging.info(
        "Starting Weather Intelligence Dashboard..."
    )

    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False,
    )