from dash import ctx, dcc, html
import dash_bootstrap_components as dbc

def add_axis(remove_y, n_clicks, existing_children, file_headers, id):
    button_clicked = ctx.triggered_id
    if isinstance(button_clicked, dict) and button_clicked["type"] == "remove-y":
        index_to_remove = None
        for index, item in enumerate(remove_y):
            if item is not None:
                index_to_remove = index
                break
        if index_to_remove is not None:
            updated_children = (
                existing_children[:index_to_remove]
                + existing_children[index_to_remove + 1 :]
            )
            return updated_children, id

    if n_clicks is not None and n_clicks > 0:
        number_of_rows = len(existing_children)
        new_content = dbc.Row(
            [
                dbc.Col(dbc.Label("Y-Axis:"), width="auto"),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id={"type": "add-y", "index": id},
                            options=file_headers,
                            value=[],
                            multi=True,
                            placeholder="Select y axis",
                            style={
                                "alignSelf": "center",
                                "minWidth": "250px"
                            },
                        ),
                        dbc.Input(
                            id={"type": "y-label", "index": id},
                            placeholder="Enter axis name",
                            type="text",
                            className="m-2 float-right w-40",
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-x-square")],
                            class_name="m-2",
                            id={"type": "remove-y", "index": id},
                        ),
                    ],
                    id="y-axes-selection",
                    style={"display": "flex"},
                ),
            ],
            class_name="align-items-center",
        )
        button_content = dbc.Row(
            [dbc.Button("Add axis", id="add-y-btn")], className="mx-auto w-25"
        )
        updated_children = (
            existing_children[: (number_of_rows - 1)] + [new_content] + [button_content]
        )
        return updated_children, id + 1
    return existing_children, id
