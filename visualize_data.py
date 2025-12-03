import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
file_path = "cleaned_data.csv"   

# ---------------- LOAD DATA ------------------
df = pd.read_csv("cleaned_data.csv")

selected_columns = [
    "TT_20", "PT_24", "FT_01", "FT_02", "FT_03c", "FT_07c", "FT_08c",
    "AT_03", "AT_05", "AT_01", "PT_02", "PT_21", "PT_23",
    "FT_05", "FT_06c"
]

df = df[[col for col in selected_columns if col in df.columns]]

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

categorical_cols = []   
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

# ---------------- LAYOUT ------------------
app.layout = dbc.Container([
    html.H2("📊 Sensor Data Dashboard", className="text-center mt-4 mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filters"),
                dbc.CardBody([
                    html.Label("Select Column for Pie / Bar / Line"),
                    dcc.Dropdown(
                        id="num-col",
                        options=[{"label": c, "value": c} for c in numeric_cols],
                        placeholder="Choose column"
                    html.Label("Select Column"),
                    dcc.Dropdown(
                        id="num-col",
                        options=[{"label": c, "value": c} for c in numeric_cols],
                        placeholder="Choose a column"
                    )
                ])
            ])
        ], width=3),
        # ---------------- TABS ------------------
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Line Chart", tab_id="line"),
                dbc.Tab(label="Bar Chart", tab_id="bar"),
                dbc.Tab(label="Pie Chart", tab_id="pie"),
                dbc.Tab(label="Box Chart", tab_id="box"),
                dbc.Tab(label="Data Table", tab_id="table")
            ], id="tabs", active_tab="line"),

            html.Div(id="tab-content", className="mt-3")
        ], width=9)
    ])
], fluid=True)
# ---------------- CALLBACK ------------------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
    Input("num-col", "value")
)
def render_content(tab, num):
    # Data table
    if tab == "table":
        return dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=12,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"fontWeight": "bold"}
        )
    if num is None:
        return html.H5("Please select a column from the filter panel.")

    # Line Chart
    # When no column selected
    if num is None:
        return html.H5("Please select a column from the filter panel.")

    # Line chart
    if tab == "line":
        fig = px.line(df, y=num, title=f"Line Chart: {num}")
        return dcc.Graph(figure=fig)
    # Bar Chart
    if tab == "bar":
        fig = px.bar(df, y=num, title=f"Bar Chart: {num}")
        return dcc.Graph(figure=fig)
    # Bar chart
    if tab == "bar":
        fig = px.bar(df, y=num, title=f"Bar Chart: {num}")
        return dcc.Graph(figure=fig)

    # Pie chart (rounded values)
    if tab == "pie":
        temp = df[num].round(0).astype(int)
        fig = px.pie(names=temp, title=f"Pie Chart (Binned): {num}")
        return dcc.Graph(figure=fig)
    return html.H5("Invalid selection.")
    # ⭐ NEW: Box chart
    if tab == "box":
        fig = px.box(df, y=num, title=f"Box Plot: {num}")
        return dcc.Graph(figure=fig)

    return html.H5("Invalid selection.")


# ---------------- RUN APP ------------------

if __name__ == "__main__":
    app.run(debug=True)
