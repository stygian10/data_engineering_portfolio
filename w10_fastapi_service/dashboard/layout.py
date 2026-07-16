from dash import html, dcc, dash_table

from dashboard.styles import (
    PAGE_STYLE,
    TITLE_STYLE,
    SECTION_TITLE_STYLE,
    CARD_STYLE,
    KPI_STYLE,
    ROW_STYLE,
    FILTER_CONTAINER_STYLE,
    HALF_WIDTH_CARD,
    TABLE_STYLE,
)


def create_layout():

    return html.Div(

        [

            # Page Title

            html.H1(
                "Prediction Analytics Dashboard",
                style=TITLE_STYLE,
            ),

            # Filters

            html.H2(
                "Filters",
                style=SECTION_TITLE_STYLE,
            ),

            html.Div(

                [

                    html.Div(

                        [

                            html.Label("City"),

                            dcc.Dropdown(
                                id="city-dropdown",
                                placeholder="Select a city",
                                clearable=False,
                            ),

                        ],

                        style={"flex": "1"},

                    ),

                    html.Div(

                        [

                            html.Label("Date"),

                            dcc.DatePickerSingle(
                                id="date-picker",
                                placeholder="Select a date",
                                display_format="DD MMM YYYY",
                            ),

                        ],

                        style={"flex": "1"},

                    ),

                ],

                style=FILTER_CONTAINER_STYLE,

            ),

            # Prediction Summary

            html.H2(
                "Prediction Summary",
                style=SECTION_TITLE_STYLE,
            ),

            html.Div(

                [

                    html.Div(
                        [
                            html.H4("Latest Prediction Record"),
                            html.H2(id="kpi-date"),
                        ],
                        style=KPI_STYLE,
                    ),

                    html.Div(
                        [
                            html.H4("Observed Temperature"),
                            html.H2(id="kpi-actual"),
                        ],
                        style=KPI_STYLE,
                    ),

                    html.Div(
                        [
                            html.H4("Predicted Temperature"),
                            html.H2(id="kpi-prediction"),
                        ],
                        style=KPI_STYLE,
                    ),

                    html.Div(
                        [
                            html.H4("Average Prediction Error"),
                            html.H2(id="kpi-error"),
                        ],
                        style=KPI_STYLE,
                    ),

                    html.Div(
                        [
                            html.H4("Prediction Records"),
                            html.H2(id="kpi-count"),
                        ],
                        style=KPI_STYLE,
                    ),

                ],

                style=ROW_STYLE,

            ),

            # Model Information

            html.H2(
                "Model Information",
                style=SECTION_TITLE_STYLE,
            ),

            html.Div(

                [

                    html.Table(

                        [

                            html.Tr([
                                html.Td("Prediction Model"),
                                html.Td(id="model-name"),
                            ]),

                            html.Tr([
                                html.Td("Model Accuracy (R²)"),
                                html.Td(id="model-r2"),
                            ]),

                            html.Tr([
                                html.Td("RMSE"),
                                html.Td(id="model-rmse"),
                            ]),

                            html.Tr([
                                html.Td("MAE (Training)"),
                                html.Td(id="model-mae"),
                            ]),

                            html.Tr([
                                html.Td("Training Dataset"),
                                html.Td(id="model-dataset"),
                            ]),

                        ],

                        id="model-information-table",

                    ),

                ],

                style=CARD_STYLE,

            ),

            # Model Performance

            html.H2(
                "Model Performance",
                style=SECTION_TITLE_STYLE,
            ),

            html.Div(

                [

                    html.Div(
                        dcc.Graph(id="prediction-chart"),
                        style=HALF_WIDTH_CARD,
                    ),

                    html.Div(
                        dcc.Graph(id="error-chart"),
                        style=HALF_WIDTH_CARD,
                    ),

                ],

                style=ROW_STYLE,

            ),

            # Prediction Results

            html.H2(
                "Prediction Results",
                style=SECTION_TITLE_STYLE,
            ),

            html.Div(

                [

                    dash_table.DataTable(

                        id="prediction-table",

                        columns=[
                            {
                                "name": "Date",
                                "id": "date",
                            },
                            {
                                "name": "City",
                                "id": "city",
                            },
                            {
                                "name": "Observed (°C)",
                                "id": "target_temp_next_day",
                            },
                            {
                                "name": "Predicted (°C)",
                                "id": "predicted_temperature",
                            },
                            {
                                "name": "Error (°C)",
                                "id": "prediction_error",
                            },
                        ],

                        data=[],

                        page_size=10,

                        sort_action="native",

                        style_table={
                            "overflowX": "auto",
                        },

                        style_cell={
                            "textAlign": "center",
                            "padding": "10px",
                            "fontFamily": "Arial",
                        },

                        style_header={
                            "fontWeight": "bold",
                        },

                    ),

                ],

                style=TABLE_STYLE,

            ),

        ],

        style=PAGE_STYLE,

    )