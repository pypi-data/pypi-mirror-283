from dash import dcc, html
import dash_bootstrap_components as dbc


def generate_graph(figure):
    HTML_GRAPH = dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(
                        [
                            dcc.Store(id="point-index"),
                            dcc.Input(
                                id="traces",
                                placeholder="Select a trace",
                                style={"width": "300px"},
                                disabled=True,
                            ),
                            html.Button("<", id="left", disabled=True),
                            html.Button(">", id="right", disabled=True),
                            html.Button("clear", id="clear", disabled=True),
                        ],
                        style={
                            "backgroundColor": "white",
                            "display": "flex",
                        },
                    ),
                    html.Div(
                        [dcc.Graph(id="graph", figure=figure)],
                        style={
                            "justifyContent": "center",
                            "alignItems": "center",
                            "margin" : "auto"
                        },
                    ),
                ]
            )
        ],
        className="m-4",
    )
    return HTML_GRAPH
