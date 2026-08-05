import pandas as pd
from dash import Input, Output, dash_table, dcc, html

from .data_loader import load_weather_data


# Load data once when the application starts
df = load_weather_data()

df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.date


app_layout = html.Div(
    [
        html.H1("Weather Intelligence Dashboard"),

        html.Br(),

        html.Label("Select City"),

        dcc.Dropdown(
            id="city-dropdown",
            options=[
                {"label": city, "value": city}
                for city in sorted(df["city"].unique())
            ],
            value=sorted(df["city"].unique())[0],
            clearable=False,
        ),

        html.Br(),

        html.Label("Select Date Range"),

        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=df["date"].min(),
            max_date_allowed=df["date"].max(),
            start_date=df["date"].min(),
            end_date=df["date"].max(),
        ),

        html.Br(),
        html.Br(),

        dash_table.DataTable(
            id="weather-table",
            page_size=20,
            sort_action="native",
            filter_action="native",
            style_table={"overflowX": "auto"},
        ),
    ]
)


def register_callbacks(app):
    """Register dashboard callbacks."""

    @app.callback(
        Output("weather-table", "data"),
        Output("weather-table", "columns"),
        Input("city-dropdown", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
    )
    def update_table(city, start_date, end_date):

        filtered_df = df.copy()

        filtered_df = filtered_df[
            filtered_df["city"] == city
        ]

        filtered_df = filtered_df[
            (filtered_df["date"] >= pd.to_datetime(start_date).date())
            & (filtered_df["date"] <= pd.to_datetime(end_date).date())
        ]

        return (
            filtered_df.to_dict("records"),
            [{"name": col, "id": col} for col in filtered_df.columns],
        )
    