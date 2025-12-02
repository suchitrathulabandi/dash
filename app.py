from dash import Dash, html, dcc
import plotly.express as px

app = Dash(__name__)

fig = px.line(x=[1, 2, 3], y=[10, 15, 13], title="Sample Line Chart")

app.layout = html.Div([
    html.H1("My First Dash App"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)