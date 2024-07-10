from amplabs.components.axisSelection import default_card_content
from amplabs.components.appLayout import setup_layout
from amplabs.callbacks.addAnnotation import add_annotation, update_navigation_buttons
from amplabs.callbacks.updateLineChart import update_line_chart
from amplabs.callbacks.readFile import read_file, add_transformation, load_file_from_sidebar
from amplabs.callbacks.addAxis import add_axis
from amplabs.callbacks.updateLineChart import update_output
from amplabs.callbacks.directoryTree import (
	update_directory_tree,
	open_dialogue_box,
	toggle_file_offcanvas,
)
import json, os
from amplabs.callbacks.updateLayout import update_style_after_load


def call_dash_app():
	from dash import (
		Dash,
		Input,
		Output,
		State,
		ALL,
		clientside_callback,
		ClientsideFunction,
	)
	from dash.exceptions import PreventUpdate
	import dash_bootstrap_components as dbc
	import dash_mantine_components as dmc
	from dash_iconify import DashIconify

	app = Dash(
		__name__,
		external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
		suppress_callback_exceptions=True,
	)
	app.index_string = """
	                   <!DOCTYPE html>
	                   <html>
	                   <head>
	                       {%metas%}
	                       <title>{%title%}</title>
	                       {%favicon%} {%css%}
	                       <style>
	                       .mantine-Notifications-root {
	                           position: fixed !important;
	                           top: 10px !important;
	                           left: 50% !important;
	                           transform: translateX(-50%) !important;
	                           z-index: 9999 !important;
	                       }
	                       </style>
	                   </head>
	                   <body>
	                       {%app_entry%}
	                       <footer>{%config%} {%scripts%} {%renderer%}</footer>
	                       <script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
	                       <script
	                       src="src-ace/ace.js"
	                       type="text/javascript"
	                       charset="utf-8"
	                       ></script>
	                   </body>
	                   </html>
	                   """
	os.environ["REACT_VERSION"] = "18.2.0"
	app.layout = setup_layout

	@app.callback(
		Output("axis-selection-bar-container", "children"),
		Input("file-headers", "data"),
		Input("edited-yaml-store", "data"),
		State("yaml-store", "data"),
	)
	def update_axis_selection_bar(file_headers, edited_json, data):
		if len(file_headers) == 0:
			raise PreventUpdate
		if isinstance(data, str):
			json_config = json.loads(data)
		elif isinstance(data, dict):
			json_config = data
		else:
			json_config = {}
		json_config = json_config if json_config is not None else {}
		return default_card_content(file_headers, json_config)

	app.callback(
		Output("directory-tree", "children"),
		Output("file-offcanvas", "is_open", allow_duplicate=True),
		Input("directory-file-path", "data"),
		prevent_initial_call=True,
	)(update_directory_tree)

	app.callback(
		Output("directory-file-path", "data"),
		Input("open-directory-btn", "n_clicks"),
		Input("folder-open-home-btn", "n_clicks"),
		prevent_initial_call=True,
	)(open_dialogue_box)

	app.callback(
		Output("left", "disabled"),
		Output("right", "disabled"),
		Output("clear", "disabled"),
		Input("traces", "value"),
	)(update_navigation_buttons)

	app.callback(
		Output("graph", "figure", allow_duplicate=True),
		Output("traces", "value"),
		Output("point-index", "data"),
		Input("graph", "clickData"),
		State("graph", "figure"),
		State("point-index", "data"),
		State("traces", "value"),
		State({"type": "add-x", "index": 0}, "value"),
		Input("left", "n_clicks"),
		Input("right", "n_clicks"),
		Input("clear", "n_clicks"),
		State("file-data", "data"),
		prevent_initial_call=True,
	)(add_annotation)

	app.callback(
		Output("graph", "figure", allow_duplicate=True),
		Output("updated-size", "data"),
		Input({"type": "add-x", "index": ALL}, "value"),
		[Input({"type": "add-y", "index": ALL}, "value")],
		Input({"type": "x-label", "index": ALL}, "value"),
		[Input({"type": "y-label", "index": ALL}, "value")],
		Input("edited-yaml-store", "data"),
		State("file-data", "data"),
		State("updated-size", "data"),
		State("yaml-store", "data"),
		prevent_initial_call=True,
	)(update_line_chart)

	app.callback(
		Output("file-data", "data", allow_duplicate=True),
		Output("file-headers", "data", allow_duplicate=True),
		Output("uploaded-file-list", "children", allow_duplicate=True),
		Output("transformed-column-list", "data", allow_duplicate=True),
		Input("upload-data", "contents"),
		State("upload-data", "filename"),
		State("upload-data", "last_modified"),
		prevent_initial_call=True,
	)(read_file)

	app.callback(
		Output("file-data", "data", allow_duplicate=True),
		Output("file-headers", "data", allow_duplicate=True),
		Output("transformed-column-list", "data", allow_duplicate=True),
		Input("yaml-store", "data"),
		State("file-data", "data"),
		prevent_initial_call=True,
	)(add_transformation)

	app.callback(
		Output("all-y-dropdowns", "children"),
		Output("axis-id", "data"),
		Input({"type": "remove-y", "index": ALL}, "n_clicks"),
		[Input("add-y-btn", "n_clicks")],
		[State("all-y-dropdowns", "children")],
		State("file-headers", "data"),
		State("axis-id", "data"),
		prevent_initial_call=True,
	)(add_axis)

	clientside_callback(
		ClientsideFunction(namespace="clientside", function_name="handle_sidebar"),
		Output("offcanvas", "is_open"),
		Input("open-offcanvas", "n_clicks"),
		Input("yaml-store", "data"),
		State("offcanvas", "is_open"),
		prevent_initial_call=True,
	)

	clientside_callback(
		ClientsideFunction(namespace="clientside", function_name="handle_save_config"),
		Output("yaml-store", "data"),
		Input("save-config", "n_clicks"),
		State("yaml-store", "data"),
		prevent_initial_call=True,
	)

	app.callback(
		Output("edited-yaml-store", "data"),
		Input("yaml-store", "data"),
		[State("offcanvas", "is_open")],
		prevent_initial_call=True,
	)(update_output)

	clientside_callback(
		ClientsideFunction(namespace="clientside", function_name="adjust_plot_size"),
		Output("dummy", "data"),
		Input("updated-size", "data"),
		State("yaml-store", "data"),
	)

	app.callback(
		Output("file-offcanvas", "is_open", allow_duplicate=True),
		Input("open-file-offcanvas", "n_clicks"),
		[State("file-offcanvas", "is_open")],
		prevent_initial_call=True,
	)(toggle_file_offcanvas)

	app.callback(
		Output("file-data", "data"),
		Output("file-headers", "data"),
		Output("uploaded-file-list", "children"),
		Output("transformed-column-list", "data"),
		Input({"type": "list-directory-files", "index": ALL}, "n_clicks"),
		State("yaml-store", "data"),
		prevent_initial_call=True,
	)(load_file_from_sidebar)

	app.callback(
		Output("upload-data", "style"),
		Output("folder-open-home-btn", "style"),
		Output("complete-upload-layout", "style"),
		Output("chart-area", "style"),
		Output("open-offcanvas", "style"),
		Output("open-file-offcanvas", "style"),
		Output("title-header", "style"),
		Output("or-div", "style"),
		Output("save-config", "children"),
		Input("file-data", "data"),
		Input("directory-file-path", "data"),
		prevent_initial_call=True,
	)(update_style_after_load)

	@app.callback(
		Output("notifications-container", "children"),
		Input("transformed-column-list", "data"),
		prevent_initial_call=True,
	)
	def show(show_list):
		if len(show_list) == 0:
			raise PreventUpdate
		dmc_list = dmc.List([dmc.ListItem(f"{item}") for item in show_list])
		return dmc.Notification(
			title=f"Hey! These new columns are added using configs",
			id="simple-notify",
			action="show",
			message=dmc_list,
			icon=DashIconify(icon="icon-park-outline:transform"),
		)

	global dash_server_running
	app.run(debug=True, port=8050)


call_dash_app()
