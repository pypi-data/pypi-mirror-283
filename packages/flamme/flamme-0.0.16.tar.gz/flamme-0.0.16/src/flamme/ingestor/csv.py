r"""Contain the implementation of a CSV ingestor."""

from __future__ import annotations

__all__ = ["CsvIngestor"]

import logging
from typing import TYPE_CHECKING, Any

import pandas as pd

from flamme.ingestor.base import BaseIngestor
from flamme.utils.path import human_file_size, sanitize_path

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class CsvIngestor(BaseIngestor):
    r"""Implement a CSV DataFrame ingestor.

    Args:
        path: The path to the CSV file to ingest.
        **kwargs: Additional keyword arguments for
            ``pandas.read_csv``.

    Example usage:

    ```pycon

    >>> from flamme.ingestor import ParquetIngestor
    >>> ingestor = ParquetIngestor(path="/path/to/frame.csv")
    >>> ingestor
    ParquetIngestor(path=/path/to/frame.csv)
    >>> frame = ingestor.ingest()  # doctest: +SKIP

    ```
    """

    def __init__(self, path: Path | str, **kwargs: Any) -> None:
        self._path = sanitize_path(path)
        self._kwargs = kwargs

    def __repr__(self) -> str:
        args = ", ".join([f"{key}={value}" for key, value in self._kwargs.items()])
        if args:
            args = ", " + args
        return f"{self.__class__.__qualname__}(path={self._path}{args})"

    def ingest(self) -> pd.DataFrame:
        logger.info(f"Ingesting CSV data from {self._path} (size={human_file_size(self._path)})...")
        frame = pd.read_csv(filepath_or_buffer=self._path, **self._kwargs)
        logger.info(f"Data ingested. DataFrame shape: {frame.shape}")
        return frame
