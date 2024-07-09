import sys,pkg_resources, subprocess
from dash import html
import dash_bootstrap_components as dbc
from amplabs.components.fileTree import FileTree


def update_directory_tree(file_path):
	if file_path is None:
		return [
			html.Div("You have not yet opened a folder."),
			dbc.Button(
				"Open Folder",
				id="open-directory-btn",
				style={"display": "flex", "margin": "8px auto"},
			),
		], False
	return FileTree(file_path).render(), True


def open_dialogue_box(n_clicks1, n_clicks2):
	if n_clicks1 or n_clicks2:
		file_dialog_path = pkg_resources.resource_filename('amplabs.utils', 'fileDialog.py')
		result = subprocess.run(
			[sys.executable, file_dialog_path], capture_output=True, text=True
		)
		folder_path = result.stdout.strip()
		if folder_path == "No folder selected":
			return None
		return folder_path
	return None


def toggle_file_offcanvas(n1, is_open):
	if n1:
		return not is_open
	return is_open
