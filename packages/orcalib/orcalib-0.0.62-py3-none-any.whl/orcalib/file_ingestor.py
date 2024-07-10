import json
import pickle
from abc import ABC
from collections import Counter
from typing import Any, Hashable, Union, cast
from urllib.request import urlopen

import numpy as np
import pandas
from datasets import Dataset, DatasetDict, load_dataset
from tqdm.auto import trange

from orca_common import RowDict
from orcalib.database import OrcaDatabase, TableCreateMode, TableHandle
from orcalib.orca_types import (
    DocumentT,
    DocumentTypeHandle,
    FloatT,
    Int8T,
    IntT,
    OrcaTypeHandle,
    TextT,
    VectorT,
)


class FileIngestorBase(ABC):
    """Base class for file ingestors"""

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset: list[dict[Hashable, Any]],
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
        """
        if auto_table and not replace:
            assert table_name not in db.tables, "Table already exists - can't use auto_table"
        self._db = db
        self._table_name = table_name
        self._dataset = dataset
        self._auto_table = auto_table
        self._replace = replace
        self._convert_to_hashable_format = True

    def _schema_from_dataset(self, sample: dict[Hashable, Any]) -> dict[str, OrcaTypeHandle]:
        """Infer schema from the dataset"""
        schema = {}

        for col in sample.keys():
            if isinstance(sample[col], str):
                if len(sample[col]) > 100:
                    schema[col] = DocumentT
                else:
                    schema[col] = TextT
            elif isinstance(sample[col], int):
                schema[col] = IntT
            elif isinstance(sample[col], float):
                schema[col] = FloatT
            elif isinstance(sample[col], bool):
                # TODO: use BoolT when it's implemented
                schema[col] = Int8T
            elif isinstance(sample[col], list):
                schema[col] = VectorT[len(sample[col])]
            else:
                raise ValueError(f"Can't infer type for column {col}")
        return schema

    def _df_to_row_dict_list(self, df: pandas.DataFrame) -> list[dict]:
        """Convert DataFrame to list of dicts, similar to to_dict(orient="records") but handles arrays"""
        dataset = []
        columns = df.columns.values.tolist()
        for i in trange(len(df)):
            curr_row = df.iloc[i].tolist()
            for j in range(len(curr_row)):
                # Process vectors and numpy integers
                if isinstance(curr_row[j], str) and curr_row[j][0] == "[":
                    if curr_row[j][-1] != "]":
                        raise Exception("Incorrectly formatted list in CSV file")
                    curr_row[j] = [float(x.strip()) for x in curr_row[j][1 : len(curr_row[j]) - 1].split(",")]
                elif isinstance(curr_row[j], np.integer):
                    curr_row[j] = int(curr_row[j])
                elif isinstance(curr_row[j], np.ndarray):
                    curr_row[j] = list(curr_row[j])
            dataset.append(dict(zip(columns, curr_row)))
        return dataset

    def _create_table(self) -> Any:
        schema = self._schema_from_dataset(self._dataset[0])
        print(f"Creating table {self._table_name} with schema {schema}")
        return self._db.create_table(
            self._table_name,
            if_table_exists=(
                TableCreateMode.REPLACE_CURR_TABLE if self._replace else TableCreateMode.ERROR_IF_TABLE_EXISTS
            ),
            **schema,
        )

    def run(self, only_create_table: bool = False, skip_create_table: bool = False) -> TableHandle:
        """
        Ingest the data into the database table

        Args:
            only_create_table: Whether to only create the table and not ingest the data
            skip_create_table: Whether to skip creating the table

        Returns:
            A handle to the table that was created
        """
        if self._auto_table and not skip_create_table:
            table = self._create_table()
        else:
            table = self._db[self._table_name]
            # Convert file schema to hashable format with strings so we can use Counter
            file_col_types = []
            for file_col in self._schema_from_dataset(self._dataset[0]).values():
                if isinstance(file_col, DocumentTypeHandle):
                    file_col_types.append("text")
                else:
                    file_col_types.append(file_col.full_name)
            # Do the same for the schema of the existing table
            curr_col_types = []
            for table_col in table.columns:
                col_type = table.columns[table_col].dtype
                # Just like above, we treat text and document as the same type
                if col_type == "document":
                    curr_col_types.append("text")
                else:
                    curr_col_types.append(col_type)
            # Raise exception if the file schema does not match the table schema
            if self._auto_table and Counter(file_col_types) != Counter(curr_col_types):
                raise Exception("File schema does not match table schema")
        # ingest the data
        if not only_create_table:
            table.insert(*cast(list[dict[str, Any]], list(self._dataset)))
        return table


class PickleIngestor(FileIngestorBase):
    """
    Ingestor for [Pickle][pickle] files

    Examples:
        >>> ingestor = PickleIngestor(db, "my_table", "data.pkl", auto_table=True)
        >>> table = ingestor.run()
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
        """
        if dataset_path[0:4] == "http":
            with urlopen(dataset_path) as f:
                dataset = pickle.load(f)
        else:
            with open(dataset_path, "rb") as f:
                dataset = pickle.load(f)
        FileIngestorBase.__init__(self, db, table_name, dataset, auto_table, replace)


class JSONIngestor(FileIngestorBase):
    """
    Ingestor for JSON files

    Examples:
        >>> ingestor = JSONIngestor(db, "my_table", "data.json", auto_table=True)
        >>> table = ingestor.run()
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
        """
        if dataset_path[0:4] == "http":
            with urlopen(dataset_path) as f:
                json_dataset = json.load(f)
        else:
            with open(dataset_path, "r") as f:
                json_dataset = json.load(f)
        if isinstance(json_dataset, list):
            dataset = json_dataset
        elif "data" in json_dataset:
            dataset = json_dataset["data"]
        else:
            raise Exception("Incorrectly formatted JSON file")
        FileIngestorBase.__init__(self, db, table_name, dataset, auto_table, replace)


class JSONLIngestor(FileIngestorBase):
    """
    Ingestor for [JSONL](https://jsonlines.org/) files

    Examples:
        >>> ingestor = JSONLIngestor(db, "my_table", "data.jsonl", auto_table=True)
        >>> table = ingestor.run()
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
        """
        dataset = []
        if dataset_path[0:4] == "http":
            with urlopen(dataset_path) as f:
                for line in f:
                    dataset.append(json.loads(line))
        else:
            with open(dataset_path, "r") as f:
                for line in f:
                    dataset.append(json.loads(line))
        FileIngestorBase.__init__(self, db, table_name, dataset, auto_table, replace)


class CSVIngestor(FileIngestorBase):
    """
    Ingestor for CSV files

    Examples:
        >>> ingestor = CSVIngestor(db, "my_table", "data.csv", auto_table=True)
        >>> table = ingestor.run()
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
        """
        df = pandas.read_csv(dataset_path)
        FileIngestorBase.__init__(self, db, table_name, self._df_to_row_dict_list(df), auto_table, replace)


class ParquetIngestor(FileIngestorBase):
    """
    Ingestor for [Parquet](https://parquet.apache.org/) files

    Examples:
        >>> ingestor = ParquetIngestor(db, "my_table", "data.parquet", auto_table=True)
        >>> table = ingestor.run()
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
        """
        try:
            import pyarrow
        except ImportError:
            raise ImportError("Please install pyarrow to use the ParquetIngestor")

        df = pyarrow.parquet.read_table(dataset_path).to_pandas()
        FileIngestorBase.__init__(self, db, table_name, self._df_to_row_dict_list(df), auto_table, replace)


class HFDatasetIngestor(FileIngestorBase):
    """
    [HuggingFace Dataset](https://huggingface.co/datasets) Ingestor

    Examples:
        >>> ingestor = HFDatasetIngestor(db, "my_table", "imdb", split="train")
        >>> table = ingestor.run()
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset: Dataset | str,
        auto_table: bool = False,
        replace: bool = False,
        split: str | None = None,
        cache_dir: str | None = None,
    ):
        """
        Initialize the ingestor

        Args:
            db: The database to ingest into
            table_name: The name of the table to ingest the data into
            dataset: The dataset to ingest
            auto_table: Whether to automatically create the table if it doesn't exist
            replace: Whether to replace the table if it already exists
            split: The split of the dataset to ingest
            cache_dir: The directory to cache the dataset in
        """
        if auto_table and not replace:
            assert table_name not in db.tables, "Table already exists - can't use auto_table"
        self._db = db
        self._table_name = table_name
        if isinstance(dataset, str):
            temp = load_dataset(dataset, cache_dir=cache_dir)
            if isinstance(temp, DatasetDict):
                temp = temp[split or "train"]
            assert isinstance(temp, Dataset)
            self._dataset = temp
        else:
            self._dataset = dataset
        self._auto_table = auto_table
        self._replace = replace
