import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px

df = pd.read_csv("car_price_prediction_.csv")


app = Dash(__name__)


app.layout = html.Div([
    html.H1("Car Price Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label("Select Brand"),
            dcc.Dropdown(
                id="brand-filter",
                options=[{"label": b, "value": b} for b in df["Brand"].unique()],
                value=None,
                placeholder="Select a brand",
                clearable=True
            )
        ], style={"width": "30%", "display": "inline-block"}),
        html.Div([
            html.Label("Select Fuel Type"),
            dcc.Dropdown(
                id="fuel-filter",
                options=[{"label": f, "value": f} for f in df["Fuel Type"].unique()],
                value=None,
                placeholder="Select fuel type",
                clearable=True
            )
        ], style={"width": "30%", "display": "inline-block", "marginLeft": "2%"}),
        html.Div([
            html.Label("Select Transmission"),
            dcc.Dropdown(
                id="transmission-filter",
                options=[{"label": t, "value": t} for t in df["Transmission"].unique()],
                value=None,
                placeholder="Select transmission type",
                clearable=True
            )
        ], style={"width": "30%", "display": "inline-block", "marginLeft": "2%"}),
    ]),

    html.Br(),

    # Graph
    dcc.Graph(id="price-graph"),

    html.Br(),

    # Data Table
    html.H3("Filtered Data Preview"),
    dash_table.DataTable(
        id="data-table",
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
        style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"}
    )
])

@app.callback(
    [Output("price-graph", "figure"),
     Output("data-table", "data")],
    [
        Input("brand-filter", "value"),
        Input("fuel-filter", "value"),
        Input("transmission-filter", "value")
    ]
)
def update_dashboard(brand, fuel, transmission):

    # Filter logic
    filtered_df = df.copy()

    if brand:
        filtered_df = filtered_df[filtered_df["Brand"] == brand]

    if fuel:
        filtered_df = filtered_df[filtered_df["Fuel Type"] == fuel]

    if transmission:
        filtered_df = filtered_df[filtered_df["Transmission"] == transmission]

    # Graph
    if filtered_df.empty:
        fig = px.scatter(title="No data for selected filters")
    else:
        fig = px.scatter(
            filtered_df,
            x="Engine Size",
            y="Price",
            color="Fuel Type",
            size="Mileage",
            hover_data=["Model", "Year", "Condition"],
            title="Price vs Engine Size",
        )

    # Table Data
    table_data = filtered_df.to_dict("records")

    return fig, table_data

if __name__ == "__main__":
    app.run(debug=True)
