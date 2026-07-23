from dash import dcc, html
from dash.dash_table import DataTable


# Page styling

PAGE_STYLE = {
    "fontFamily": "Arial, sans-serif",
    "padding": "30px",
    "backgroundColor": "#f5f5f5",
}


SECTION_STYLE = {
    "backgroundColor": "white",
    "padding": "20px",
    "marginBottom": "30px",
    "borderRadius": "8px",
    "boxShadow": "0 2px 6px rgba(0,0,0,0.15)",
}


ROW_STYLE = {
    "display": "flex",
    "gap": "20px",
    "marginBottom": "20px",
}


KPI_STYLE = {
    "flex": "1",
    "padding": "15px",
    "textAlign": "center",
    "backgroundColor": "#fafafa",
    "borderRadius": "8px",
    "boxShadow": "0 1px 4px rgba(0,0,0,0.15)",
}


SOURCE_STYLE = {
    "marginBottom": "20px",
    "padding": "10px",
    "backgroundColor": "#f8f9fa",
    "borderLeft": "4px solid #0074D9",
    "fontSize": "14px",
    "color": "#444444",
}


TABLE_STYLE = {
    "overflowX": "auto",
}



# Reusable Components

def create_kpi_card(title, component_id):
    """
    Create a reusable KPI card.
    """

    return html.Div(
        [
            html.H4(title),
            html.H2(id=component_id),
        ],
        style=KPI_STYLE,
    )


def create_source_box(text):
    """
    Create a reusable data source information box.
    """

    return html.Div(
        [
            html.B("Source: "),
            html.Span(text),
        ],
        style=SOURCE_STYLE,
    )


def create_model_row(title, component_id):
    """
    Create a reusable model information row.
    """

    return html.Tr(
        [
            html.Th(title),
            html.Td(id=component_id),
        ]
    )

# Live Prediction Section


live_prediction_section = html.Div(

    [

        html.H2("Live Prediction"),

        create_source_box(
            "Week 7 Feature Engineering Dataset "
            "(w7_features_final.parquet) "
            "served through the Week 10 FastAPI "
            "prediction service."
        ),

        html.Label("Select City"),

        dcc.Dropdown(
            id="city-dropdown",
            placeholder="Select a city",
            clearable=False,
        ),

        html.Br(),

        html.H3("Prediction Summary"),

        html.Div(

            [

                create_kpi_card(
                    "Current Hour",
                    "latest-update",
                ),

                create_kpi_card(
                    "Current Temperature",
                    "current-temperature",
                ),

                create_kpi_card(
                    "Predicted Temperature",
                    "predicted-temperature",
                ),

                create_kpi_card(
                    "Prediction Difference",
                    "prediction-difference",
                ),

            ],

            style=ROW_STYLE,

        ),

        html.H3("Model Information"),

        html.P(

            [

                html.B("Model: "),
                html.Span(id="model-name"),

                "   |   ",

                html.B("R² Score: "),
                html.Span(id="model-r2"),

                "   |   ",

                html.B("RMSE: "),
                html.Span(id="model-rmse"),

                "   |   ",

                html.B("MAE: "),
                html.Span(id="model-mae"),

                "   |   ",

                html.B("Dataset: "),
                html.Span(id="model-dataset"),

                "   |   ",

                html.B("Last Trained: "),
                html.Span(id="model-trained-at"),

            ],

            style={
                "fontSize": "16px",
                "lineHeight": "1.8",
            },

        ),

    ],

    style=SECTION_STYLE,

)



# Historical Prediction Section


historical_prediction_section = html.Div(

    [

        html.H2("Historical Prediction"),

        create_source_box(
            "Week 9 Prediction Dataset "
            "(weather_predictions.csv)"
        ),

        html.Label("Select City"),

        dcc.Dropdown(
            id="history-city-dropdown",
            placeholder="Select a city",
            clearable=False,
        ),

        html.Br(),

        html.Label("Select Date"),

        dcc.DatePickerSingle(
            id="history-date-picker",
            display_format="DD MMM YYYY",
            placeholder="All Dates",
        ),

        html.Br(),
        html.Br(),

        html.H3("Historical Prediction Records"),

        DataTable(

            id="prediction-table",

            columns=[
                {
                    "name": "Date & Time",
                    "id": "time",
                },
                {
                    "name": "City",
                    "id": "city",
                },
                {
                    "name": "Actual Temperature (°C)",
                    "id": "target_temp_next_hour",
                },
                {
                    "name": "Predicted Temperature (°C)",
                    "id": "predicted_temperature",
                },
                {
                    "name": "Prediction Error (°C)",
                    "id": "prediction_error",
                },
            ],

            data=[],

            page_size=10,

            sort_action="native",

            style_table=TABLE_STYLE,

            style_cell={
                "textAlign": "center",
                "padding": "10px",
            },

            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f2f2f2",
            },

        ),

    ],

    style=SECTION_STYLE,

)



# Historical Model Performance Section


historical_performance_section = html.Div(

    [

        html.H2("Historical Model Performance"),

        dcc.Graph(
            id="actual-vs-predicted-chart",
            config={
                "displayModeBar": False,
            },
        ),

        html.Br(),

        dcc.Graph(
            id="prediction-error-chart",
            config={
                "displayModeBar": False,
            },
        ),

    ],

    style=SECTION_STYLE,

)


# Dashboard Layout


layout = html.Div(

    [

        html.H1(

            "Weather Prediction Analytics Dashboard",

            style={
                "textAlign": "center",
                "marginBottom": "30px",
            },

        ),

        live_prediction_section,

        historical_prediction_section,

        historical_performance_section,

    ],

    style=PAGE_STYLE,

)



# Layout Factory


def create_layout():
    """
    Return the dashboard layout.
    """

    return layout