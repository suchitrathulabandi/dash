import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px

df = pd.read_csv("car_price_prediction_.csv")
print(df.head())
app=Dash(__name__)
app.layout = html.Div([
    html.H1("Car Price Dashboard", style={"textAlign": "center"}),

    
    html.Label("Select Fuel Type:"),
    dcc.Dropdown(
        id="fuel-dropdown",
        options=[{"label": ft, "value": ft} for ft in df["Fuel_Type"].unique()],
        value=df["Fuel_Type"].unique()[0],  
        clearable=False
    ),

    html.Br(),
    dcc.Graph(id="price-graph"),

    html.Br(),

    # Data Table
    html.H3("Dataset Preview"),
    dash_table.DataTable(
        id="table",
        data=df.head(20).to_dict("records"),   # show first 20 rows
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"}
    )
])
@app.callback(
    Output("price-graph", "figure"),
    Input("fuel-dropdown", "value")
)
def update_graph(selected_fuel):
    filtered_df = df[df["Fuel_Type"] == selected_fuel]

    fig = px.scatter(
        filtered_df,
        x="Present_Price",
        y="Selling_Price",
        color="Transmission",
        title=f"Selling Price vs Present Price ({selected_fuel})",
        size="Kms_Driven",
        hover_data=["Car_Name"]
    )
    return fig
if __name__ == "__main__":
    app.run_serverpython(debug=True)
