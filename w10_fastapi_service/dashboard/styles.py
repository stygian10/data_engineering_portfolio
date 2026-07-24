# Color palette

COLORS = {
    "background": "#f4f7fb",
    "card": "#ffffff",
    "primary": "#1f2c3d",
    "secondary": "#6b7a90",
    "border": "#dce3ec",
}


# Main page

PAGE_STYLE = {
    "backgroundColor": COLORS["background"],
    "padding": "20px",
    "minHeight": "100vh",
}


# Page title

TITLE_STYLE = {
    "color": COLORS["primary"],
    "fontSize": "34px",
    "fontWeight": "bold",
    "marginBottom": "20px",
}


# Section heading

SECTION_TITLE_STYLE = {
    "color": COLORS["primary"],
    "fontSize": "22px",
    "fontWeight": "600",
    "marginBottom": "12px",
}


# Shared card style

CARD_STYLE = {
    "backgroundColor": COLORS["card"],
    "padding": "16px",
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
    "marginBottom": "16px",
}


# KPI card

KPI_STYLE = {
    **CARD_STYLE,
    "flex": "1",
    "minWidth": "180px",
    "textAlign": "center",
}


# Dashboard row

ROW_STYLE = {
    "display": "flex",
    "flexWrap": "wrap",
    "gap": "16px",
    "marginBottom": "16px",
}


# Two-column chart layout

HALF_WIDTH_CARD = {
    **CARD_STYLE,
    "flex": "1",
    "minWidth": "45%",
}


# Full-width chart layout

FULL_WIDTH_CARD = {
    **CARD_STYLE,
    "width": "100%",
}


# Filter section

FILTER_CONTAINER_STYLE = {
    **CARD_STYLE,
    "display": "flex",
    "gap": "16px",
    "alignItems": "center",
    "flexWrap": "wrap",
}


# Table container

TABLE_STYLE = {
    **CARD_STYLE,
    "overflowX": "auto",
}

# Model Information

MODEL_INFO_CONTAINER_STYLE = {
    **CARD_STYLE,
}

MODEL_INFO_TABLE_STYLE = {
    "width": "100%",
    "borderCollapse": "collapse",
}

MODEL_LABEL_STYLE = {
    "padding": "14px",
    "fontWeight": "600",
    "color": COLORS["primary"],
    "borderBottom": f"1px solid {COLORS['border']}",
    "width": "35%",
    "textAlign": "left",
}

MODEL_VALUE_STYLE = {
    "padding": "14px",
    "color": COLORS["secondary"],
    "borderBottom": f"1px solid {COLORS['border']}",
    "textAlign": "left",
}
