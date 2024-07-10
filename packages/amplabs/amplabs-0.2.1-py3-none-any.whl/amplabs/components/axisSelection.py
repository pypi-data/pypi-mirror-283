from dash import dcc, html
import dash_bootstrap_components as dbc
import fnmatch


def default_y_dropdowns(file_headers, json_config):
    items = []
    try:
        y_axis = {
            k: v
            for k, v in json_config["graph_settings"]["y_axis"].items()
            if k != "default"
        }
    except KeyError:
        y_axis = {"y1": {"columns": [], "label": ""}}
    for index, (key, value) in enumerate(y_axis.items()):
        axis_value = value.get("columns", [])
        if value.get("wildcard_matching", False):
            column_list = [
                header
                for header in file_headers
                if fnmatch.fnmatch(header.lower(), axis_value.lower())
            ]
        else:
            column_list = (
                axis_value if isinstance(axis_value, list) else axis_value.split(",")
            )
        items.append(
            dbc.Row(
                [
                    dbc.Col(dbc.Label("Y-Axis:"), width="auto"),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id={"type": "add-y", "index": index},
                                options=file_headers,
                                value=column_list,
                                multi=True,
                                clearable=True,
                                placeholder="Select y axis",
                                style={
                                    "alignSelf": "center",
                                    "minWidth": "250px",
                                },
                            ),
                            dbc.Input(
                                id={"type": "y-label", "index": index},
                                placeholder="Enter axis name",
                                type="text",
                                className="m-2 float-right w-40",
                                value=value.get("label", {}).get("text", ""),
                            ),
                            dbc.Button(
                                [html.I(className="bi bi-x-square")],
                                class_name="m-2",
                                id={"type": "remove-y", "index": index},
                            ),
                        ],
                        id="y-axes-selection",
                        style={"display": "flex"},
                    ),
                ],
                class_name="align-items-center",
            ),
        )
    items.append(
        dbc.Row(
            [dbc.Button("Add axis", id="add-y-btn")],
            className="mx-auto w-25",
        )
    )
    return items


def default_layout_dropdowns(file_headers, json_config):
    try:
        x_axis = json_config["graph_settings"]["x_axis"]
    except:
        x_axis = {"columns": "", "label": ""}
    x_column = x_axis.get("columns", "")
    x_label = x_axis.get("label", {}).get("text", "")
    dropdownLayout = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(dbc.Label("X-Axis:"), width="auto"),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id={"type": "add-x", "index": 0},
                                        options=file_headers,
                                        value=x_column,
                                        placeholder="Select x axis",
                                        style={
                                            "width": "100%",
                                            "display": "block",
                                            "alignSelf": "center",
                                        },
                                    ),
                                    dbc.Input(
                                        id={"type": "x-label", "index": 0},
                                        placeholder="Enter axis name",
                                        type="text",
                                        className="m-2 float-right w-50",
                                        style={"minWidth": "130px"},
                                        value=x_label,
                                    ),
                                ],
                                className="d-flex",
                            ),
                        ],
                        class_name="align-items-center",
                    ),
                ],
                width=4,
            ),
            dbc.Col(
                default_y_dropdowns(file_headers, json_config),
                id="all-y-dropdowns",
            ),
        ],
    )
    return dropdownLayout


def default_card_content(file_headers, json_config):
    return [
        dbc.CardHeader("Select Axes for plot"),
        dbc.CardBody(default_layout_dropdowns(file_headers, json_config)),
    ]
