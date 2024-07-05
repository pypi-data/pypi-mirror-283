r"""Contain the implementation of sections to analyze the number null
values."""

from __future__ import annotations

__all__ = ["NullValueSection"]

import logging
from typing import TYPE_CHECKING

import pandas as pd
from coola.utils import repr_indent, repr_mapping
from jinja2 import Template
from matplotlib import pyplot as plt

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)
from flamme.utils.figure import figure2html, readable_xticklabels

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np


logger = logging.getLogger(__name__)


class NullValueSection(BaseSection):
    r"""Implement a section that analyzes the number of null values.

    Args:
        columns: The column names.
        null_count: The number of null values for each column.
        total_count: The total number of values for each column.
        figsize: The figure size in inches. The first dimension
            is the width and the second is the height.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> from flamme.section import NullValueSection
    >>> section = NullValueSection(
    ...     columns=["col1", "col2", "col3"],
    ...     null_count=np.array([0, 1, 2]),
    ...     total_count=np.array([5, 5, 5]),
    ... )
    >>> section
    NullValueSection(
      (columns): ('col1', 'col2', 'col3')
      (null_count): array([0, 1, 2])
      (total_count): array([5, 5, 5])
      (figsize): None
    )
    >>> section.get_statistics()
    {'columns': ('col1', 'col2', 'col3'), 'null_count': (0, 1, 2), 'total_count': (5, 5, 5)}

    ```
    """

    def __init__(
        self,
        columns: Sequence[str],
        null_count: np.ndarray,
        total_count: np.ndarray,
        figsize: tuple[float, float] | None = None,
    ) -> None:
        self._columns = tuple(columns)
        self._null_count = null_count.flatten().astype(int)
        self._total_count = total_count.flatten().astype(int)
        self._figsize = figsize

        if len(self._columns) != self._null_count.shape[0]:
            msg = (
                f"columns ({len(self._columns):,}) and null_count ({self._null_count.shape[0]:,}) "
                "do not match"
            )
            raise RuntimeError(msg)
        if len(self._columns) != self._total_count.shape[0]:
            msg = (
                f"columns ({len(self._columns):,}) and total_count "
                f"({self._total_count.shape[0]:,}) do not match"
            )
            raise RuntimeError(msg)

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "columns": self._columns,
                    "null_count": self._null_count,
                    "total_count": self._total_count,
                    "figsize": self._figsize,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    @property
    def columns(self) -> tuple[str, ...]:
        r"""The columns used to compute the duplicated rows."""
        return self._columns

    @property
    def null_count(self) -> np.ndarray:
        r"""The number of null values for each column."""
        return self._null_count

    @property
    def total_count(self) -> np.ndarray:
        r"""The total number of values for each column."""
        return self._total_count

    @property
    def figsize(self) -> tuple[float, float] | None:
        r"""The individual figure size in pixels.

        The first dimension is the width and the second is the height.
        """
        return self._figsize

    def get_statistics(self) -> dict:
        return {
            "columns": self._columns,
            "null_count": tuple(self._null_count.tolist()),
            "total_count": tuple(self._total_count.tolist()),
        }

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        logger.info("Rendering the null value distribution of all columns...")
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "table_alpha": self._create_table(sort_by="column"),
                "table_sort": self._create_table(sort_by="null"),
                "bar_figure": self._create_bar_figure(),
                "num_columns": f"{len(self._columns):,}",
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
This section analyzes the number and proportion of null values for the {{num_columns}}
columns.
In the following histogram, the columns are sorted by ascending order of null values.

{{bar_figure}}

<details>
    <summary>[show statistics per column]</summary>

    <p style="margin-top: 1rem;">
    The following tables show the number and proportion of null values for the {{num_columns}}
    columns.
    The background color of the row indicates the proportion of missing values:
    dark blues indicates more missing values than light blues.

    <div class="container-fluid">
        <div class="row align-items-start">
            <div class="col align-self-center">
                <p><b>Columns sorted by alphabetical order</b></p>

                {{table_alpha}}

            </div>
            <div class="col">
                <p><b>Columns sorted by ascending order of missing values</b></p>

                {{table_sort}}

            </div>
        </div>
    </div>
</details>

<p style="margin-top: 1rem;">
"""

    def _create_bar_figure(self) -> str:
        dataframe = self._get_dataframe().sort_values(by="null")
        fig, ax = plt.subplots(figsize=self._figsize)
        labels = dataframe["column"].tolist()
        ax.bar(x=labels, height=dataframe["null"].to_numpy(), color="tab:blue")
        if labels:
            ax.set_xlim(-0.5, len(labels) - 0.5)
        readable_xticklabels(ax, max_num_xticks=100)
        ax.set_xlabel("column")
        ax.set_ylabel("number of null values")
        ax.set_title("number of null values per column")
        return figure2html(fig, close_fig=True)

    def _create_table(self, sort_by: str) -> str:
        dataframe = self._get_dataframe().sort_values(by=sort_by)
        rows = "\n".join(
            [
                create_table_row(column=column, null_count=null_count, total_count=total_count)
                for column, null_count, total_count in zip(
                    dataframe["column"].to_numpy(),
                    dataframe["null"].to_numpy(),
                    dataframe["total"].to_numpy(),
                )
            ]
        )
        return Template(
            """
<table class="table table-hover table-responsive w-auto" >
    <thead class="thead table-group-divider">
        <tr>
            <th>column</th>
            <th>null pct</th>
            <th>null count</th>
            <th>total count</th>
        </tr>
    </thead>
    <tbody class="tbody table-group-divider">
        {{rows}}
        <tr class="table-group-divider"></tr>
    </tbody>
</table>
"""
        ).render({"rows": rows})

    def _get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {"column": self._columns, "null": self._null_count, "total": self._total_count}
        )


def create_table_row(column: str, null_count: int, total_count: int) -> str:
    r"""Create the HTML code of a new table row.

    Args:
        column: The column name.
        null_count (int): The number of null values.
        total_count (int): The total number of rows.

    Returns:
        The HTML code of a row.
    """
    pct = null_count / total_count
    return Template(
        """<tr>
    <th style="background-color: rgba(0, 191, 255, {{null_pct}})">{{column}}</th>
    <td {{num_style}}>{{null_pct}}</td>
    <td {{num_style}}>{{null_count}}</td>
    <td {{num_style}}>{{total_count}}</td>
</tr>"""
    ).render(
        {
            "num_style": f'style="text-align: right; background-color: rgba(0, 191, 255, {pct})"',
            "column": column,
            "null_count": f"{null_count:,}",
            "null_pct": f"{pct:.4f}",
            "total_count": f"{total_count:,}",
        }
    )
