from dash import Input, Output
import plotly.graph_objects as go

from dashboard.prediction_loader import (
    load_prediction_data,
    get_available_cities,
    get_city_data,
    get_available_dates,
    filter_city_data,
    filter_prediction_data,
)


def register_callbacks(app):

    
    # Populate City Dropdown
    
    @app.callback(
        Output("city-dropdown", "options"),
        Input("city-dropdown", "id"),
    )
    def populate_city_dropdown(_):

        df = load_prediction_data()

        cities = get_available_cities(df)

        return [
            {
                "label": city,
                "value": city,
            }
            for city in cities
        ]

    
    # Update Available Dates
    
    @app.callback(
        Output("date-picker", "min_date_allowed"),
        Output("date-picker", "max_date_allowed"),
        Output("date-picker", "date"),
        Input("city-dropdown", "value"),
    )
    def update_available_dates(city):

        if not city:
            return (
                None,
                None,
                None,
            )

        df = load_prediction_data()

        city_df = get_city_data(
            df,
            city,
        )

        dates = get_available_dates(city_df)

        if not dates:
            return (
                None,
                None,
                None,
            )

        return (
            dates[0],
            dates[-1],
            dates[-1],
        )
    
    # Prediction Summary
    
    @app.callback(
        Output("kpi-date", "children"),
        Output("kpi-actual", "children"),
        Output("kpi-prediction", "children"),
        Output("kpi-error", "children"),
        Output("kpi-count", "children"),
        Output("model-name", "children"),
        Output("model-r2", "children"),
        Output("model-rmse", "children"),
        Output("model-mae", "children"),
        Output("model-dataset", "children"),
        Input("city-dropdown", "value"),
        Input("date-picker", "date"),
    )
    def update_prediction_summary(
        city,
        selected_date,
    ):

        if not city or not selected_date:

            return (
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            )

        df = load_prediction_data()

        filtered_df = filter_prediction_data(
            df,
            city,
            selected_date,
        )

        if filtered_df.empty:

            return (
                "N/A",
                "N/A",
                "N/A",
                "N/A",
                "0",
                "Linear Regression",
                "0.91",
                "2.05°C",
                "1.69°C",
                "0 Records",
            )

        record = filtered_df.iloc[0]

        latest_date = record["date"].strftime(
            "%d %b %Y"
        )

        actual_temperature = (
            f"{record['target_temp_next_day']:.1f}°C"
        )

        predicted_temperature = (
            f"{record['predicted_temperature']:.1f}°C"
        )

        average_error = (
            f"{filtered_df['prediction_error'].abs().mean():.2f}°C"
        )

        prediction_records = (
            f"{len(filtered_df)} Record"
        )

        return (

            latest_date,
            actual_temperature,
            predicted_temperature,
            average_error,
            prediction_records,

            "Linear Regression",
            "0.91",
            "2.05°C",
            "1.69°C",
            f"{len(df)} Records",

        )
    
    # Model Performance Charts

    @app.callback(
        Output("prediction-chart", "figure"),
        Output("error-chart", "figure"),
        Input("city-dropdown", "value"),
    )
    def update_model_performance(city):

        empty_figure = go.Figure()

        if not city:

            return (
                empty_figure,
                empty_figure,
            )

        # Load prediction data

        df = load_prediction_data()

        city_df = filter_city_data(
            df,
            city,
        )

        
        # Chart 1
        # Actual vs Predicted Temperature
        
        prediction_figure = go.Figure()

        prediction_figure.add_trace(

            go.Scatter(

                x=city_df["date"],
                y=city_df["target_temp_next_day"],

                mode="lines+markers",

                name="Observed Temperature",

            )

        )

        prediction_figure.add_trace(

            go.Scatter(

                x=city_df["date"],
                y=city_df["predicted_temperature"],

                mode="lines+markers",

                name="Predicted Temperature",

            )

        )

        prediction_figure.update_layout(

            title="Actual vs Predicted Temperature",

            template="plotly_white",

            xaxis_title="Date",

            yaxis_title="Temperature (°C)",

            hovermode="x unified",

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),

        )

        
        # Chart 2
        # Prediction Error

        error_figure = go.Figure()

        error_figure.add_trace(

            go.Scatter(

                x=city_df["date"],
                y=city_df["prediction_error"],

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

        return (

            prediction_figure,

            error_figure,

        )
    
    # Prediction Results Table
    
    @app.callback(
        Output("prediction-table", "data"),
        Input("city-dropdown", "value"),
    )
    def update_prediction_table(city):

        if not city:
            return []

        # Load prediction data

        df = load_prediction_data()

        city_df = filter_city_data(
            df,
            city,
        )

        # Select columns

        table_df = city_df[
            [
                "date",
                "city",
                "target_temp_next_day",
                "predicted_temperature",
                "prediction_error",
            ]
        ].copy()

        # Sort newest first while date is still datetime

        table_df = table_df.sort_values(
            by="date",
            ascending=False,
        )

        # Format values

        table_df["date"] = (
            table_df["date"]
            .dt.strftime("%d %b %Y")
        )

        table_df["target_temp_next_day"] = (
            table_df["target_temp_next_day"]
            .round(2)
        )

        table_df["predicted_temperature"] = (
            table_df["predicted_temperature"]
            .round(2)
        )

        table_df["prediction_error"] = (
            table_df["prediction_error"]
            .round(2)
        )

        return table_df.to_dict("records")