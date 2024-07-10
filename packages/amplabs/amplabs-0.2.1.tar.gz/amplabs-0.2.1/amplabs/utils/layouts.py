import yaml, pkg_resources

def add_borders_and_layout(fig):
    config_path = pkg_resources.resource_filename('amplabs', 'config.yaml')
    with open(config_path, "r", encoding="utf-8") as yamlfile:
        json_config = yaml.safe_load(yamlfile)
        json_config = json_config if json_config is not None else {}
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        mirror=True,
    )
    fig.update_yaxes(
        showline=True, linewidth=1, linecolor="black", mirror=True, rangemode="tozero"
    )
    width = json_config.get("plot_area", {}).get("width", None)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        height=json_config.get("plot_area", {}).get("height", 500),
        width=None if width is None else width,
        hovermode="closest",
        hoverdistance=-1,
        legend={
            "xref": "container",
            "yref": "container",
            "y": 0.9,
        },
        showlegend=True,
    )
 

colorTransitions = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#ff9896",
    "#7dba91",
    "#59a590",
    "#40908e",
    "#287a8c",
    "#1c6488",
    "#254b7f",
]
