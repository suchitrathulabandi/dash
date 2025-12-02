import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px

# Load Data
df = pd.read_csv("car_price_prediction_.csv")

# App
app = Dash(__name__)

# -----------------------------
# KPI Helper Functions
# -----------------------------
def create_kpi_card(title, value):
    return html.Div(
        [
            html.H4(title, style={"margin": "0", "color": "#555"}),
            html.H2(value, style={"margin": "0", "color": "#111"})
        ],
        style={
            "padding": "15px",
            "background": "white",
            "boxShadow": "0 3px 10px rgba(0,0,0,0.1)",
            "borderRadius": "10px",
            "width": "30%",
            "textAlign": "center",
        }
    )

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div(
    style={"padding": "20px", "fontFamily": "Arial"},
    children=[
        html.H1("Car Price Analytics Dashboard", style={"textAlign": "center"}),

        # Filters
        html.Div(
            style={"display": "flex", "justifyContent": "space-around", "marginTop": "20px"},
            children=[
                html.Div([
                    html.Label("Brand"),
                    dcc.Dropdown(
                        id="brand",
                        options=[{"label": b, "value": b} for b in df["Brand"].unique()],
                        placeholder="Select Brand",
                        clearable=True
                    )
                ], style={"width": "30%"}),

                html.Div([
                    html.Label("Fuel Type"),
                    dcc.Dropdown(
                        id="fuel",
                        options=[{"label": f, "value": f} for f in df["Fuel Type"].unique()],
                        placeholder="Select Fuel Type",
                        clearable=True
                    )
                ], style={"width": "30%"}),

                html.Div([
                    html.Label("Transmission"),
                    dcc.Dropdown(
                        id="transmission",
                        options=[{"label": t, "value": t} for t in df["Transmission"].unique()],
                        placeholder="Select Transmission",
                        clearable=True
                    )
                ], style={"width": "30%"}),
            ]
        ),

        html.Br(),

        # KPIs
        html.Div(
            id="kpi-box",
            style={"display": "flex", "justifyContent": "space-between"}
        ),

        html.Br(),

        # Graphs Row 1
        html.Div(
            style={"display": "flex", "justifyContent": "space-between"},
            children=[
                html.Div([dcc.Graph(id="scatter")], style={"width": "48%"}),
                html.Div([dcc.Graph(id="fuel-pie")], style={"width": "48%"}),
            ]
        ),

        html.Br(),

        # Graphs Row 2
        html.Div(
            style={"display": "flex", "justifyContent": "space-between"},
            children=[
                html.Div([dcc.Graph(id="brand-bar")], style={"width": "48%"}),
                html.Div([dcc.Graph(id="year-line")], style={"width": "48%"}),
            ]
        ),

        html.Br(),

        # Data Table
        html.H3("Filtered Dataset"),
        dash_table.DataTable(
            id="table",
            page_size=10,
            style_table={"overflowX": "auto"},
            style_header={"backgroundColor": "#eaeaea"},
            style_cell={"textAlign": "left", "padding": "8px"},
        )
    ]
)

# -----------------------------
# Callback
# -----------------------------
@app.callback(
    [
        Output("scatter", "figure"),
        Output("fuel-pie", "figure"),
        Output("brand-bar", "figure"),
        Output("year-line", "figure"),
        Output("table", "data"),
        Output("kpi-box", "children"),
    ],
    [
        Input("brand", "value"),
        Input("fuel", "value"),
        Input("transmission", "value"),
    ]
)
def update_dashboard(brand, fuel, transmission):

    # Filter Data
    filtered = df.copy()

    if brand:
        filtered = filtered[filtered["Brand"] == brand]
    if fuel:
        filtered = filtered[filtered["Fuel Type"] == fuel]
    if transmission:
        filtered = filtered[filtered["Transmission"] == transmission]

    # Fallback when no data
    if filtered.empty:
        return (
            px.scatter(title="No Data Found"),
            px.pie(title="No Data Found"),
            px.bar(title="No Data Found"),
            px.line(title="No Data Found"),
            [],
            []
        )

    # ---------------- Scatter Chart ----------------
    scatter_fig = px.scatter(
        filtered,
        x="Engine Size",
        y="Price",
        size="Mileage",
        color="Fuel Type",
        hover_data=["Brand", "Model", "Year", "Condition"],
        title="Price vs Engine Size"
    )

    # ---------------- Pie Chart ----------------
    pie_fig = px.pie(
        filtered,
        names="Fuel Type",
        title="Car Count by Fuel Type",
        hole=0.4
    )

    # ---------------- Bar Chart: Average Price by Brand ----------------
    brand_avg = filtered.groupby("Brand", as_index=False)["Price"].mean()
    brand_bar = px.bar(
        brand_avg,
        x="Brand",
        y="Price",
        title="Average Price by Brand",
        text_auto=".2f"
    )

    # ---------------- Line Chart: Average Price by Year ----------------
    year_avg = filtered.groupby("Year", as_index=False)["Price"].mean()
    year_line = px.line(
        year_avg,
        x="Year",
        y="Price",
        title="Average Price by Year",
        markers=True
    )

    # ---------------- KPIs ----------------
    kpi_cards = [
        create_kpi_card("Total Cars", str(len(filtered))),
        create_kpi_card("Average Price", f"${filtered['Price'].mean():,.2f}"),
        create_kpi_card("Average Mileage", f"{filtered['Mileage'].mean():,.0f} km"),
    ]

    return scatter_fig, pie_fig, brand_bar, year_line, filtered.to_dict("records"), kpi_cards


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
