r"""Contain the implementation of a section to generate a summary of a
DataFrame."""

from __future__ import annotations

__all__ = ["DataFrameSummarySection"]

import logging
from typing import TYPE_CHECKING, Any

from jinja2 import Template

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)
from flamme.utils.dtype import series_column_types

if TYPE_CHECKING:
    from collections.abc import Sequence

    import pandas as pd


logger = logging.getLogger(__name__)


class DataFrameSummarySection(BaseSection):
    r"""Implement a section that returns a summary of a DataFrame.

    Args:
        frame: The DataFrame to analyze.
        top: The number of most frequent values to show.

    Example usage:

    ```pycon

    >>> import pandas as pd
    >>> import numpy as np
    >>> from flamme.section import DataFrameSummarySection
    >>> section = DataFrameSummarySection(
    ...     frame=pd.DataFrame(
    ...         {
    ...             "col1": np.array([1.2, 4.2, 4.2, 2.2]),
    ...             "col2": np.array([1, 1, 1, 1]),
    ...             "col3": np.array([1, 2, 2, 2]),
    ...         }
    ...     )
    ... )
    >>> section
    DataFrameSummarySection(top=5)
    >>> section.get_statistics()
    {'columns': ('col1', 'col2', 'col3'), 'null_count': (0, 0, 0), 'nunique': (3, 1, 2), 'column_types': ({<class 'float'>}, {<class 'int'>}, {<class 'int'>})}
    """

    def __init__(self, frame: pd.DataFrame, top: int = 5) -> None:
        self._frame = frame
        if top < 0:
            msg = f"Incorrect top value ({top}). top must be positive"
            raise ValueError(msg)
        self._top = top

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(top={self._top})"

    @property
    def frame(self) -> pd.DataFrame:
        r"""The DataFrame to analyze."""
        return self._frame

    @property
    def top(self) -> int:
        return self._top

    def get_columns(self) -> tuple[str, ...]:
        return tuple(self._frame.columns)

    def get_null_count(self) -> tuple[int, ...]:
        return tuple(
            self._frame.isna().sum().to_frame("__count__")["__count__"].astype(int).tolist()
        )

    def get_nunique(self) -> tuple[int, ...]:
        return tuple(self._frame.nunique(dropna=False).astype(int).tolist())

    def get_column_types(self) -> tuple[set[type], ...]:
        return tuple(series_column_types(self._frame[col]) for col in self.frame)

    def get_most_frequent_values(self, top: int = 5) -> tuple[tuple[tuple[Any, int], ...], ...]:
        value_counts = []
        for col in self.frame:
            values = self._frame[col].value_counts(dropna=False, sort=True).head(top)
            value_counts.append(tuple((val, c) for val, c in zip(values.index, values.to_list())))
        return tuple(value_counts)

    def get_statistics(self) -> dict:
        return {
            "columns": self.get_columns(),
            "null_count": self.get_null_count(),
            "nunique": self.get_nunique(),
            "column_types": self.get_column_types(),
        }

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        logger.info("Rendering the DataFrame summary section...")
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "table": self._create_table(),
                "nrows": f"{self._frame.shape[0]:,}",
                "ncols": f"{self._frame.shape[1]:,}",
            }
        )

    def render_html_toc(
        self, number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
    ) -> str:
        return render_html_toc(number=number, tags=tags, depth=depth, max_depth=max_depth)

    def _create_template(self) -> str:
        return """
<h{{depth}} id="{{id}}">{{section}} {{title}} </h{{depth}}>

{{go_to_top}}

<p style="margin-top: 1rem;">
This section shows a short summary of each column.

<ul>
  <li> <b>column</b>: are the column names</li>
  <li> <b>types</b>: are the real object types for the objects in the column </li>
  <li> <b>null</b>: are the number (and percentage) of null values in the column </li>
  <li> <b>unique</b>: are the number (and percentage) of unique values in the column </li>
</ul>

<p style="margin-top: 1rem;">
<b>General statistics about the DataFrame</b>

<ul>
  <li> number of rows: {{nrows}}</li>
  <li> number of columns: {{ncols}} </li>
</ul>

{{table}}
<p style="margin-top: 1rem;">
"""

    def _create_table(self) -> str:
        total = self._frame.shape[0]
        return create_table(
            columns=self.get_columns(),
            null_count=self.get_null_count(),
            nunique=self.get_nunique(),
            column_types=self.get_column_types(),
            most_frequent_values=self.get_most_frequent_values(top=self._top),
            total=total,
        )


def create_table(
    columns: Sequence[str],
    null_count: Sequence[int],
    nunique: Sequence[int],
    column_types: Sequence[set],
    most_frequent_values: Sequence[Sequence[tuple[Any, int]]],
    total: int,
) -> str:
    rows = []
    for (
        column,
        null,
        nuniq,
        types,
        mf_values,
    ) in zip(columns, null_count, nunique, column_types, most_frequent_values):
        rows.append(
            create_table_row(
                column=column,
                null=null,
                types=types,
                nunique=nuniq,
                most_frequent_values=mf_values,
                total=total,
            )
        )
    rows = "\n".join(rows)
    return Template(
        """
<table class="table table-hover table-responsive w-auto" >
<thead class="thead table-group-divider">
    <tr>
        <th>column</th>
        <th>types</th>
        <th>null</th>
        <th>unique</th>
        <th>most frequent values</th>
    </tr>
</thead>
<tbody class="tbody table-group-divider">
    {{rows}}
    <tr class="table-group-divider"></tr>
</tbody>
</table>
"""
    ).render({"rows": rows})


def create_table_row(
    column: str,
    null: int,
    nunique: int,
    types: set,
    most_frequent_values: Sequence[tuple[Any, int]],
    total: int,
) -> str:
    r"""Create the HTML code of a new table row.

    Args:
        column: The column name.
        null: The number of null values.
        nunique: The number of unique values.
        types: The types in th column.
        most_frequent_values: The most frequent values.
        total: The total number of rows.

    Returns:
        The HTML code of a row.
    """
    total = max(total, 1)
    types = ", ".join(sorted([prepare_type_name(t) for t in types]))
    null = f"{null:,} ({100 * null / total:.2f}%)"
    nunique = f"{nunique:,} ({100 * nunique / total:.2f}%)"
    most_frequent_values = ", ".join(
        [f"{val} ({100 * c / total:.2f}%)" for val, c in most_frequent_values]
    )
    return Template(
        """<tr>
    <th>{{column}}</th>
    <td>{{types}}</td>
    <td {{num_style}}>{{null}}</td>
    <td {{num_style}}>{{nunique}}</td>
    <td>{{most_frequent_values}}</td>
</tr>"""
    ).render(
        {
            "num_style": 'style="text-align: right;"',
            "column": column,
            "null": null,
            "types": types,
            "nunique": nunique,
            "most_frequent_values": most_frequent_values,
        }
    )


TYPE_NAMES = {
    "pandas._libs.tslibs.timestamps.Timestamp": "pandas.Timestamp",
    "pandas._libs.tslibs.nattype.NaTType": "pandas.NaTType",
    "pandas._libs.missing.NAType": "pandas.NAType",
}


def prepare_type_name(typ: type) -> str:
    r"""Return a compact type name when possible.

    Args:
        typ: The input type.

    Returns:
        The compact type name.
    """
    name = str(typ).split("'", maxsplit=2)[1].rsplit("'", maxsplit=2)[0]
    # Reduce the name if possible
    return TYPE_NAMES.get(name, name)
