from dash.exceptions import PreventUpdate
from dash import ctx
from amplabs.utils.afterFileUpload import (
    uploadLayout,
    openFolderBtn,
    openEditorBtn,
    openFolderHomeBtn,
    chartArea,
    completeUploadLayout,
    titleHeader,
)


def update_style_after_load(file_data, path_data):
    if file_data is None and path_data is None:
        raise PreventUpdate
    return (
        uploadLayout,
        openFolderHomeBtn,
        completeUploadLayout,
        chartArea,
        openEditorBtn,
        openFolderBtn,
        titleHeader,
        {"display": "none"},
        "Save and Apply",
    )
