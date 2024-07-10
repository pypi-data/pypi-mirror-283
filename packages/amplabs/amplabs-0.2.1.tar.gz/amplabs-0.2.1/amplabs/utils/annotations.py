
def create_annotations(x, y, yref, bgcolor, point_index):
    return dict(
        x=x,
        y=y,
        xref="x",
        yref=yref,
        text=f"x={x}<br>y={y}<br>index={point_index}",
        showarrow=True,
        font=dict(family="Courier New, monospace", size=16, color="#ffffff"),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=40,
        ay=-60,
        bordercolor="#c7c7c7",
        borderwidth=2,
        borderpad=2,
        bgcolor=bgcolor,
    )