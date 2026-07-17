from datetime import timedelta

import plotly.graph_objects as go
from dash import Input, Output

from dashboard.api_client import request_prediction

from dashboard.live_prediction_loader import (
    get_available_cities,
    load_live_prediction_data,
    validate_today_record,
)

from dashboard.prediction_loader import (
    filter_city_data,
    get_available_dates,
    load_prediction_data,
)


def register_callbacks(app):

    # Live city dropdown

    @app.callback(
        Output("live-city-dropdown", "options"),
        Input("live-city-dropdown", "id"),
    )
    def populate_live_city_dropdown(_):

        df = load_live_prediction_data()
        cities = get_available_cities(df)

        return [{"label": city, "value": city} for city in cities]
    
        # Live prediction summary

    @app.callback(

        Output("kpi-date", "children"),
        Output("kpi-actual", "children"),
        Output("kpi-prediction", "children"),
        Output("kpi-error", "children"),

        Output("kpi-next-date", "children"),
        Output("kpi-next-actual", "children"),
        Output("kpi-next-prediction", "children"),
        Output("kpi-next-error", "children"),

        Output("model-name", "children"),
        Output("model-r2", "children"),
        Output("model-rmse", "children"),
        Output("model-mae", "children"),
        Output("model-dataset", "children"),

        Input("live-city-dropdown", "value"),

    )
    def update_live_prediction(city):

        if not city:

            return (
                "", "", "", "",
                "", "", "", "",
                "", "", "", "", ""
            )

        status, message, record = validate_today_record(city)

        if not status:

            return (
                "Unavailable",
                "--",
                message,
                "--",

                "--",
                "--",
                "--",
                "--",

                "Linear Regression",
                "0.91",
                "2.05°C",
                "1.69°C",
                "120 Records",
            )
        
        
        prediction = request_prediction(record)

        

        if prediction is None:

            return (
                record["date"].strftime("%d %b %Y"),
                f"{record['temperature']:.1f}°C",
                "FastAPI Unavailable",
                "--",

                "--",
                "--",
                "--",
                "--",

                "Linear Regression",
                "0.91",
                "2.05°C",
                "1.69°C",
                "120 Records",
            )

        predicted_temperature = prediction["predicted_temperature"]

        df = load_live_prediction_data()

        today_date_value = record["date"]

        today_row = df[
            (df["city"] == city)
            & (df["date"] == today_date_value)
        ].iloc[0]

        tomorrow_date_value = today_date_value + timedelta(days=1)

        tomorrow_rows = df[
            (df["city"] == city)
            & (df["date"] == tomorrow_date_value)
        ]

        today_date = today_date_value.strftime("%d %b %Y")

        today_temperature = round(
            today_row["target_temp_next_day"],
            2,
        )

        today_error = round(
            abs(today_temperature - predicted_temperature),
            2,
        )

        next_day = tomorrow_date_value.strftime("%d %b %Y")

        if not tomorrow_rows.empty:

            tomorrow_temperature = round(
                tomorrow_rows.iloc[0]["target_temp_next_day"],
                2,
            )

        else:

            tomorrow_temperature = None

        tomorrow_prediction = round(
            predicted_temperature,
            2,
        )

        if tomorrow_temperature is not None:

            tomorrow_error = round(
                abs(
                    tomorrow_temperature - tomorrow_prediction
                ),
                2,
            )

        else:

            tomorrow_error = None
        return (

            today_date,
            f"{today_temperature:.2f}°C",
            f"{predicted_temperature:.2f}°C",
            f"{today_error:.2f}°C",

            next_day,
            f"{tomorrow_temperature:.2f}°C" if tomorrow_temperature is not None else "--",
            f"{tomorrow_prediction:.2f}°C",
            f"{tomorrow_error:.2f}°C" if tomorrow_error is not None else "--",

            "Linear Regression",
            "0.91",
            "2.05°C",
            "1.69°C",
            "120 Records",

        )
        # Historical city dropdown

    @app.callback(
        Output("history-city-dropdown", "options"),
        Input("history-city-dropdown", "id"),
    )
    def populate_history_city_dropdown(_):

        df = load_prediction_data()
        cities = sorted(df["city"].unique())

        return [{"label": city, "value": city} for city in cities]


    # Historical date picker

    @app.callback(
        Output("history-date-picker", "min_date_allowed"),
        Output("history-date-picker", "max_date_allowed"),
        Output("history-date-picker", "date"),
        Input("history-city-dropdown", "value"),
    )
    def update_history_date_picker(city):

        if not city:
            return None, None, None

        df = load_prediction_data()
        city_df = filter_city_data(df, city)
        dates = get_available_dates(city_df)

        if not dates:
            return None, None, None

        return dates[0], dates[-1], None

    # Historical prediction table

    @app.callback(
        Output("prediction-table", "data"),
        Input("history-city-dropdown", "value"),
        Input("history-date-picker", "date"),
    )
    def update_prediction_table(city, selected_date):

        if not city:
            return []

        df = load_prediction_data()
        table_df = filter_city_data(df, city)

        # Apply optional date filter

        if selected_date:
            table_df = table_df[table_df["date"] == selected_date]

        if table_df.empty:
            return []

        # Sort newest records first

        table_df = table_df.sort_values("date", ascending=False)

        # Select table columns

        table_df = table_df[
            [
                "date",
                "city",
                "target_temp_next_day",
                "predicted_temperature",
                "prediction_error",
            ]
        ].copy()

        # Format values

        table_df["date"] = table_df["date"].dt.strftime("%d %b %Y")
        table_df["target_temp_next_day"] = table_df["target_temp_next_day"].round(2)
        table_df["predicted_temperature"] = table_df["predicted_temperature"].round(2)
        table_df["prediction_error"] = table_df["prediction_error"].round(2)

        return table_df.to_dict("records")
    
        # Historical model performance charts

    @app.callback(
        Output("actual-vs-predicted-chart", "figure"),
        Output("prediction-error-chart", "figure"),
        Input("history-city-dropdown", "value"),
        Input("history-date-picker", "date"),
    )
    def update_historical_charts(city, selected_date):

        empty_figure = go.Figure()

        if not city:
            return empty_figure, empty_figure

        df = load_prediction_data()
        chart_df = filter_city_data(df, city)

        # Apply optional date filter

        if selected_date:
            chart_df = chart_df[chart_df["date"] == selected_date]

        if chart_df.empty:
            return empty_figure, empty_figure

        chart_df = chart_df.sort_values("date")

        # Actual vs predicted temperature chart

        prediction_figure = go.Figure()

        prediction_figure.add_trace(
            go.Scatter(
                x=chart_df["date"],
                y=chart_df["target_temp_next_day"],
                mode="lines+markers",
                name="Observed",
            )
        )

        prediction_figure.add_trace(
            go.Scatter(
                x=chart_df["date"],
                y=chart_df["predicted_temperature"],
                mode="lines+markers",
                name="Predicted",
            )
        )

        prediction_figure.update_layout(
            title="Observed vs Predicted Temperature",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            hovermode="x unified",
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "right",
                "x": 1,
            },
        )

        # Prediction error chart

        error_figure = go.Figure()

        error_figure.add_trace(
            go.Scatter(
                x=chart_df["date"],
                y=chart_df["prediction_error"],
                mode="lines+markers",
                name="Prediction Error",
            )
        )

        error_figure.add_hline(
            y=0,
            line_dash="dash",
            line_color="red",
        )

        error_figure.update_layout(
            title="Prediction Error Over Time",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Prediction Error (°C)",
            hovermode="x unified",
            showlegend=False,
        )

        return prediction_figure, error_figure
    


    