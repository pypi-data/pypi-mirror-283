from dash import ctx
import plotly.graph_objects as go
import pandas as pd
from dash.exceptions import PreventUpdate
from amplabs.utils.annotations import create_annotations

def add_annotation(
        clickData,
        figure,
        data,
        trace,
        x_axis,
        left_click,
        right_click,
        clear_clicks,
        dfs,
    ):
        button_clicked = ctx.triggered_id
        if not button_clicked:
            raise PreventUpdate

        new_figure = go.Figure(figure)
        new_annotation = {}

        if button_clicked == "graph":
            if not clickData:
                raise PreventUpdate
            point = clickData["points"][0]
            x = point["x"]
            y = point["y"]
            trc = []
            for i, val in enumerate(new_figure["data"]):
                trc.append(val["name"])
            point_index = point["pointIndex"]
            trace = trc[point["curveNumber"]]
            prev_mode = new_figure["data"][point["curveNumber"]]["mode"]
            color = new_figure["data"][point["curveNumber"]]["line"]["color"]
            yref = new_figure["data"][point["curveNumber"]]["yaxis"]
            new_annotation = create_annotations(
                x=x, y=y, yref=yref, bgcolor=color, point_index=point_index + 1
            )

        elif button_clicked in ("left", "right"):
            if data is None:
                raise PreventUpdate

            if button_clicked == "left":
                point_index = data - 1
            else:
                point_index = data + 1

            content = pd.DataFrame(dfs)

            if not (0 <= point_index < len(content)):
                raise PreventUpdate

            # x = content["Test Time(min)"][point_index]
            x = content[x_axis][point_index]
            y = content[trace][point_index]
            yref = new_figure["layout"]["annotations"][0]["yref"]
            color = new_figure["layout"]["annotations"][0]["bgcolor"]
            new_annotation = create_annotations(
                x=x, y=y, yref=yref, bgcolor=color, point_index=point_index + 1
            )

        elif button_clicked == "clear":
            if data is None:
                raise PreventUpdate
            new_figure["layout"]["annotations"] = []
            return new_figure, "", None
        new_figure.update_layout(annotations=[new_annotation])
        return new_figure, trace, point_index


def update_navigation_buttons(value):
    if value is None or value == "":
        return True, True, True
    return False, False, False