from dash import ctx
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
from amplabs.utils.layouts import colorTransitions, add_borders_and_layout
import json, yaml,pkg_resources


def update_line_chart(
	x_axes, y_axes_values, x_label, y_labels, store_data, dfs, isUpdated, json_config
):
	if dfs is None:
		raise PreventUpdate
	x_axes = x_axes[0]
	x_label = x_label[0]
	if x_axes == "" or not any(len(x) >= 1 for x in y_axes_values):
		raise PreventUpdate
	if ctx.triggered_id == "updated-size" and isUpdated is True:
		raise PreventUpdate
	json_config = json.loads(json_config)
	fig = go.Figure()
	count_any_color = 0
	colors_default = (
		json_config.get("graph_settings", {})
		.get("traces", {})
		.get("default", {})
		.get("color", [])
	)
	colors_default.extend(colorTransitions)
	default_y_font = (
		json_config.get("graph_settings", {})
		.get("y_axis", {})
		.get("default", {})
		.get("label", None)
		.get("font", None)
	)
	for i, y_values in enumerate(y_axes_values):
		if len(y_values) == 0:
			continue
		axis_num = i + 1
		series_name = f"y{axis_num}"
		try:
			colors = json_config["graph_settings"]["traces"][series_name]["color"]
		except:
			colors = None
		df = pd.DataFrame(dfs)
		if i == 0:
			for j, y_axis in enumerate(y_values):
				try:
					color = colors[j]
				except:
					try:
						color = colors_default[count_any_color]
						count_any_color = count_any_color + 1
					except:
						color = None
				y_df = df[y_axis]
				x_df = df[x_axes]
				fig.add_trace(
					go.Scatter(
						x=x_df,
						y=y_df,
						mode="lines",
						name=y_axis,
						yaxis="y",
						line=dict(color=color),
					)
				)
			fig.update_layout(
				yaxis=dict(
					title=dict(
						text=y_labels[i],
						font=json_config.get("graph_settings", {})
						.get("y_axis", {})
						.get(f"y{axis_num}", {})
						.get("label", {})
						.get("font", default_y_font),
					),
					ticks="outside",
				)
			)
		else:
			for j, y_axis in enumerate(y_values):
				try:
					color = colors[j]
				except:
					try:
						color = colors_default[count_any_color]
						count_any_color = count_any_color + 1
					except:
						color = None
				y_df = [float(temp) for temp in df[y_axis]]
				x_df = [float(temp) for temp in df[x_axes]]
				fig.add_trace(
					go.Scatter(
						x=x_df,
						y=y_df,
						name=y_axis,
						yaxis=f"y{axis_num}",
						line=dict(
							color=color,
						),
					)
				)
				fig.update_layout(
					**{
						f"yaxis{axis_num}": dict(
							title=dict(
								text=y_labels[i],
								font=json_config.get("graph_settings", {})
								.get("y_axis", {})
								.get(f"y{axis_num}", {})
								.get("label", {})
								.get("font", default_y_font),
							),
							overlaying="y",
							side="right",
							autoshift=True,
							anchor="free",
							ticks="outside",
							shift=20 * (i - 1),
						)
					}
				)
	fig.update_layout(
		xaxis=dict(
			title=dict(
				text=x_label,
				font=json_config.get("graph_settings", {})
				.get("x_axis", {})
				.get("label", {})
				.get("font", None),
			),
			ticks="outside",
		),
		title=dict(
			font=json_config.get("graph_settings", {})
			.get("title", {})
			.get("font", None),
			text=json_config.get("graph_settings", {})
			.get("title", {})
			.get("text", None),
			x=json_config.get("graph_settings", {})
			.get("title", {})
			.get("position", None),
		),
	)
	add_borders_and_layout(fig)
	return fig, False


def update_output(data, is_open):
	if data:
		config_path = pkg_resources.resource_filename('amplabs', 'config.yaml')
		with open(config_path, "w") as file:
			yaml.dump(json.loads(data), file)

		return f"Editor content: {data}", not is_open
	return "No content yet.", not is_open
