"""Main module."""
import pandas as pd
import plotly
import plotly.express as px


def ecdf(
    df: pd.DataFrame,
    value,
    weight=None,
    color=None,
    facet_col=None,
    facet_row=None,
    **args,
) -> plotly.graph_objects.Figure:
    """Generate ECDF plot with similar API to plotly.express plot functions

    Args:
        df (pd.DataFrame): DataFrame to pull column data from
        value (str): Value column name to be assigned to the x-axis
        weight (str, optional): Weight column name to multiply with the value
            column before computing the ECDF. Defaults to None.
        color (str, optional): Column name to which will define color groups.
            Defaults to None.
        facet_col (str, optional): Column name to define facet columns.
            Defaults to None.
        facet_row (str, optional): Column name to define facet rows. Defaults
            to None.

    Returns:
        plotly.graph_objects.Figure: A plotly Figure object
    """

    df = df.sort_values(value, ascending=True).copy()
    if weight is None:
        weight = "_weight_"
        df[weight] = 1
    groupby_cols = []
    if color is None:
        df["_color_"] = 1
        groupby_cols.append("_color_")
    else:
        groupby_cols.append(color)
    if facet_col is not None:
        groupby_cols.append(facet_col)
    if facet_row is not None:
        groupby_cols.append(facet_row)
    df_list = []
    for name, group in df.groupby(groupby_cols):
        group = group.copy()
        group["ECDF"] = group[weight].cumsum() / group[weight].sum()
        df_list.append(group)
    df = pd.concat(df_list, ignore_index=True)
    fig = px.line(
        df,
        x=value,
        y="ECDF",
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        **args,
    )
    fig.update_traces(line_shape="hv", mode="lines+markers")

    return fig
