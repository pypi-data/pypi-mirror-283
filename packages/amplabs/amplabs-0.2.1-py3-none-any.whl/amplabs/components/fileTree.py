import os
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash import html


class FileTree:
	def __init__(self, filepath: os.PathLike):
		"""
		Usage: component = FileTree('Path/to/my/File').render()
		"""
		self.filepath = filepath

	def render(self) -> dmc.Accordion:
		return dmc.Accordion(
			children=self.build_tree(self.filepath),
			multiple=True,
			className="accordion",
			chevronPosition="left",
			id="directory-tree",
		)

	def flatten(self, l):
		return [item for sublist in l for item in sublist]

	def make_file(self, file_name, file_path):
		return dmc.Text(
			[
				DashIconify(icon="akar-icons:file"),
				file_name,
				html.Button(
					DashIconify(icon="tabler:upload"),
					className="upload-btn-sidebar",
					id={"type": "list-directory-files", "index": file_path},
					title="Load File",
				),
			],
			className="file-item",
		)

	def make_folder(self, folder_name):
		return [DashIconify(icon="akar-icons:folder"), " ", folder_name]

	def build_tree(self, path):
		items = []
		if os.path.isdir(path):
			if os.path.basename(path) == "node_modules":
				return items # Skip node_modules folder
			try:
				children = self.flatten(
					[
						self.build_tree(os.path.join(path, x))
						for x in os.listdir(path)
						if (x.endswith(".csv") or os.path.isdir(os.path.join(path, x)))
						and not x.startswith(".")
					]
				)
				if children:
					items.append(
						dmc.AccordionItem(
							children=[
								dmc.AccordionControl(
									self.make_folder(os.path.basename(path))
								),
								dmc.AccordionPanel(children=children),
							],
							value=str(path),
						)
					)
			except OSError as e:
				print(f"Error accessing directory {path}: {e}")
		elif path.endswith(".csv") and not os.path.basename(path).startswith("."):
			items.append(self.make_file(os.path.basename(path), os.path.abspath(path)))
		return items
