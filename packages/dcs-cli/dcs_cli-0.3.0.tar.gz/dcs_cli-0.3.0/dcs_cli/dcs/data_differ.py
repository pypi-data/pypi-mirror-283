#  Copyright 2022-present, the Waterdip Labs Pvt. Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import glob
import os
from datetime import datetime
from time import time

import rich
from rich.console import Console

from data_diff import TableSegment, connect_to_table, diff_tables

from .models.data_diff_models import Comparison
from .serializer import serialize_table_schema
from .table import create_table_schema_row_count, differ_rows
from .themes import theme_1
from .utils import (
    analyze_diff_rows,
    calculate_column_differences,
    count_duplicates_pks,
    duck_db_load_csv_to_table,
    find_identical_columns,
    generate_table_name,
)


def diff_db_tables(
    config: Comparison,
    is_cli: bool = False,
    show_stats: bool = False,
    save_html: bool = False,
    html_path: str = "datadiff_report.html",
):
    console = Console(record=True)
    created_at = datetime.now().isoformat()
    start_time = time()
    algorithm = "hashdiff"
    source_file_path = config.source.filepath
    target_file_path = config.target.filepath
    database_type_src = config.source.driver if config.source.driver != "duckdb" else "file"
    database_type_tgt = config.target.driver if config.target.driver != "duckdb" else "file"

    if config.source.driver == "duckdb":
        if config.source.filepath is None:
            raise ValueError("File path is required for DuckDB")

        if config.source.filepath.endswith(".csv"):
            if duck_db_load_csv_to_table(config, config.source.filepath, is_source=True) is False:
                raise ValueError("Error in loading CSV to DuckDB for the source")
    if config.target.driver == "duckdb":
        if config.target.filepath is None:
            raise ValueError("File path is required for DuckDB")

        if config.target.filepath.endswith(".csv"):
            if duck_db_load_csv_to_table(config, config.target.filepath, is_source=False) is False:
                raise ValueError("Error in loading CSV to DuckDB for the target")

    table1: TableSegment = connect_to_table(
        {
            "driver": config.source.driver,
            "user": config.source.username,
            "password": config.source.password,
            "database": config.source.database,
            "schema": config.source.schema_name,
            "filepath": config.source.filepath,
            "warehouse": config.source.warehouse,
            "role": config.source.role,
            "account": config.source.account,
        },
        config.source.table,
        tuple(config.primary_keys_source),
        extra_columns=tuple(config.source_columns),
    )

    table2: TableSegment = connect_to_table(
        {
            "driver": config.target.driver,
            "user": config.target.username,
            "password": config.target.password,
            "database": config.target.database,
            "schema": config.target.schema_name,
            "filepath": config.target.filepath,
            "warehouse": config.target.warehouse,
            "role": config.target.role,
            "account": config.target.account,
        },
        config.target.table,
        tuple(config.primary_keys_target),
        extra_columns=tuple(config.target_columns),
    )
    db1_name = config.source.database if config.source.database is not None else "source"
    db2_name = config.target.database if config.target.database is not None else "target"

    # For column mappings
    columns_order_wise_src = config.primary_keys_source + config.source_columns
    columns_order_wise_target = config.primary_keys_target + config.target_columns

    diff_iter = diff_tables(table1, table2, algorithm=algorithm)

    schema_1 = table1.get_schema()
    schema_2 = table2.get_schema()
    schema_1_list = []
    schema_2_list = []

    for _, v in schema_1.items():
        schema_1_list.append(serialize_table_schema(v))
    schema_2 = table2.get_schema()
    for _, v in schema_2.items():
        schema_2_list.append(serialize_table_schema(v))

    # Column mappings
    columns_mappings = []
    schema_1_list = sorted(schema_1_list, key=lambda x: x["column_name"].upper())
    schema_2_list = sorted(schema_2_list, key=lambda x: x["column_name"].upper())

    for src, trg in zip(columns_order_wise_src, columns_order_wise_target):
        columns_mappings.append({"source": src, "target": trg})

    source_dataset = {
        "database_type": database_type_src,
        "table_name": table1.table_path[0],
        "schema": table1.database.default_schema,
        "database": db1_name,
        "primary_keys": list(table1.key_columns),
        "file_path": source_file_path,
        "files": (
            [] if source_file_path is None else [generate_table_name(csv, False) for csv in glob.glob(source_file_path)]
        ),
        "row_count": table1.count(),
        "columns": schema_1_list,
        "exclusive_cnt": 0,
        "duplicate_cnt": 0,
        "null_pk_cnt": 0,
    }
    target_dataset = {
        "database_type": database_type_tgt,
        "table_name": table2.table_path[0],
        "schema": table2.database.default_schema,
        "file_path": target_file_path,
        "files": (
            [] if target_file_path is None else [generate_table_name(csv, False) for csv in glob.glob(target_file_path)]
        ),
        "database": db2_name,
        "primary_keys": list(table2.key_columns),
        "row_count": table2.count(),
        "columns": schema_2_list,
        "exclusive_cnt": 0,
        "duplicate_cnt": 0,
        "null_pk_cnt": 0,
    }
    try:
        stats = diff_iter.get_stats_dict()
        stats.pop("stats")
        source_dataset["exclusive_cnt"] = stats["exclusive_A"]
        target_dataset["exclusive_cnt"] = stats["exclusive_B"]
        stats.update(
            {
                "table_a_row_count": source_dataset["row_count"],
                "table_b_row_count": target_dataset["row_count"],
                "diff_pks": (stats["rows_A"] + stats["rows_B"]) / target_dataset["row_count"],
                "diff_rows": stats["updated"] / source_dataset["row_count"],
                "identical_columns": find_identical_columns(schema_1_list, schema_2_list),
            }
        )
        stats.pop("rows_A")
        stats.pop("rows_B")
        stats.pop("unchanged")
    except:
        stats = {}
    columns_with_unmatched_data_type, columns_not_compared = calculate_column_differences(
        schema_1_list, schema_2_list, columns_mappings
    )
    stats.update(
        {
            "columns_with_unmatched_data_type": columns_with_unmatched_data_type,
            "columns_not_compared": columns_not_compared,
        }
    )
    et = time() - start_time
    finished_at = datetime.now().isoformat()

    response = {
        "source_dataset": source_dataset,
        "target_dataset": target_dataset,
        "stats": stats,
        "columns_mappings": columns_mappings,
        "meta": {
            "created_at": created_at,
            "seconds": et,
            "finished_at": finished_at,
        },
    }
    table = differ_rows(diff_iter, response)

    src_duplicates_pks, trg_duplicates_pks = count_duplicates_pks(
        response["diff_rows"], config.primary_keys_source, config.primary_keys_target
    )
    response["source_dataset"]["duplicate_cnt"] = src_duplicates_pks
    response["target_dataset"]["duplicate_cnt"] = trg_duplicates_pks
    if is_cli:
        create_table_schema_row_count(response, table, console)
        if save_html:
            console.save_html(html_path, theme=theme_1, clear=True)
    if show_stats:
        stats_str = diff_iter.get_stats_string()
        stats_str += f"{src_duplicates_pks} duplicate {'row' if src_duplicates_pks <= 1 else 'rows'} in source\n"
        stats_str += f"{trg_duplicates_pks} duplicate {'row' if trg_duplicates_pks <= 1 else 'rows'} in target\n"
        rich.print(stats_str)
    if config.source.driver == "duckdb":
        try:
            table1.database.close()
            os.remove(config.source.filepath)
        except:
            ...
    if config.target.driver == "duckdb":
        try:
            table2.database.close()
            os.remove(config.target.filepath)
        except:
            ...
    rows = analyze_diff_rows(response["diff_rows"], [response["source_dataset"]["primary_keys"][0]])
    response.pop("diff_rows")
    response.update(rows)
    return response
