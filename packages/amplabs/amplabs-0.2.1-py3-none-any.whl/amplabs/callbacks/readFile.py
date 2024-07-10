from amplabs.components.fileUpload import parse_contents
from dash import html, ctx
from dash.exceptions import PreventUpdate
import json, yaml, platform,pkg_resources
import pandas as pd


def read_file(
    list_of_contents,
    list_of_names,
    list_of_dates,
):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents, list_of_names, list_of_dates)
        json_config = None
        config_path = pkg_resources.resource_filename('amplabs', 'config.yaml')
        with open(config_path, "r", encoding="utf-8") as yamlfile:
            json_config = yaml.safe_load(yamlfile)
        json_config = json_config if json_config is not None else {}
        show_list = []
        df = apply_transformations(
            df, json_config.get("transformations", []), show_list
        )
        return (
            df.to_dict(orient="records"),
            df.columns.tolist(),
            html.Div([list_of_names]),
            show_list,
        )
    raise PreventUpdate


def add_transformation(config, data):
    if data is None:
        raise PreventUpdate
    json_config = json.loads(config)
    json_config = json_config if json_config is not None else {}
    df = pd.DataFrame(data)
    show_list = []
    df = apply_transformations(df, json_config.get("transformations", []), show_list)
    return df.to_dict(orient="records"), df.columns.to_list(), show_list


def load_file_from_sidebar(values, data):
    if any(x is not None for x in values):
        file_path = ctx.triggered_id["index"]
        df = pd.read_csv(file_path)
        file_name = (
            file_path.rsplit("\\", 1)[1]
            if platform.system() == "Windows"
            else file_path.rsplit("/", 1)[1]
        )
        json_config = json.loads(data)
        json_config = json_config if json_config is not None else {}
        show_list = []
        df = apply_transformations(
            df, json_config.get("transformations", []), show_list
        )
        return (
            df.to_dict(orient="records"),
            df.columns.tolist(),
            html.Div([file_name]),
            show_list,
        )
    else:
        raise PreventUpdate


def apply_transformations(df, transformations, show_list):
    for transformation in transformations:
        column = transformation["column"]
        new_column_name = transformation["new_column_name"]
        expression = transformation["expression"]

        if column in df.columns and new_column_name not in df.columns:

            def operation(x):
                return eval(expression.replace("{x}", str(x)))

            df[new_column_name] = df[column].apply(operation)
            show_list.append(new_column_name)
    return df
