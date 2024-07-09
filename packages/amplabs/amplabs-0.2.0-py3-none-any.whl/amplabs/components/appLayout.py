from amplabs.components.graph import generate_graph
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import json, yaml, pkg_resources
import plotly.graph_objects as go
from amplabs.utils.layouts import add_borders_and_layout
from amplabs.utils.beforeFileUpload import (
    uploadLayout,
    openFolderHomeBtn,
    completeUploadLayout,
    chartArea,
    openFolderBtn,
    openEditorBtn,
    titleHeader,
    openEditorBtn,
)


def setup_layout():
    figure = go.Figure()
    add_borders_and_layout(figure)
    config_path = pkg_resources.resource_filename("amplabs", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as yamlfile:
        json_config = yaml.safe_load(yamlfile)
    try:
        y_count = len(
            {
                k: v
                for k, v in json_config["graph_settings"]["y_axis"].items()
                if k != "default"
            }
        )
    except:
        y_count = 1
    return dmc.MantineProvider(
        html.Div(
            [
                dmc.NotificationProvider(position="top-left", autoClose=6000),
                html.Div(id="notifications-container"),
                html.Div(
                    [
                        html.H1(
                            "Load Your Data for Interactive Visualization",
                            style=titleHeader,
                            id="title-header",
                        ),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Load a File")],
                                className="mx-auto align-content-center",
                            ),
                            style=uploadLayout,
                        ),
                        html.Div("OR", id="or-div"),
                        dbc.Button(
                            "Open a Folder",
                            style=openFolderHomeBtn,
                            color="secondary",
                            id="folder-open-home-btn",
                        ),
                    ],
                    className="flex text-center justify-center",
                    style=completeUploadLayout,
                    id="complete-upload-layout",
                ),
                html.H5(id="uploaded-file-list", children=[], className="mx-2"),
                html.Div(
                    [
                        dcc.Store(id="file-data", data=None),
                        dcc.Store(id="file-headers", data=[]),
                        dcc.Store(id="yaml-store", data=json.dumps(json_config)),
                        dcc.Store(id="edited-yaml-store", data=[]),
                        dcc.Store(id="updated-size", data=False),
                        dcc.Store(id="dummy", data=None),
                        dcc.Store(id="directory-file-path", data=None),
                        dbc.Card(
                            id="axis-selection-bar-container",
                            color="secondary",
                            outline=True,
                            class_name="mx-4",
                        ),
                        generate_graph(figure),
                        dcc.Store(id="axis-id", data=y_count),
                        dcc.Store(id="transformed-column-list", data=[]),
                    ],
                    id="chart-area",
                    style=chartArea,
                ),
                dbc.Button(
                    [
                        html.I(className="bi bi-code-slash"),
                        html.Div("config.yaml", className="mx-2"),
                    ],
                    id="open-offcanvas",
                    n_clicks=0,
                    style=openEditorBtn,
                    color="secondary",
                    size="small",
                ),
                dbc.Button(
                    [
                        html.I(className="bi bi-folder2-open"),
                        html.Div("Explorer", className="mx-2"),
                    ],
                    id="open-file-offcanvas",
                    n_clicks=0,
                    style=openFolderBtn,
                    color="secondary",
                    size="small",
                ),
                dbc.Offcanvas(
                    children=[
                        html.Div("config.yaml"),
                        html.Pre(id="editor", style={"height": "700px"}),
                        dbc.Button("Save", id="save-config"),
                    ],
                    id="offcanvas",
                    title="Config Options",
                    is_open=False,
                    placement="end",
                    style={"width": "750px"},
                ),
                dbc.Offcanvas(
                    children=[
                        html.Div(
                            id="directory-tree",
                        )
                    ],
                    id="file-offcanvas",
                    title="File Explorer",
                    is_open=False,
                    placement="start",
                    style={"width": "350px"},
                ),
            ],
            id="main-layout",
            style={"fontSize": "14px"},
        )
    )
