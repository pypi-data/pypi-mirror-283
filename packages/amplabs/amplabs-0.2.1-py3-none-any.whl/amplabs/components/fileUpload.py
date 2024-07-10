from dash import dcc, html
import pandas as pd
import base64, io


def fileUploadDragger():
    fileupload = html.Div(
        [
            dcc.Upload(
                id="upload-data",
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                # multiple=True
            ),
            dcc.Store(id="file-data"),
        ]
    )
    return fileupload


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    df = None
    try:
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return df
