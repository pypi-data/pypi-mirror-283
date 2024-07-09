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
import uuid
from collections import defaultdict
from typing import List

import duckdb
import yaml

from .models.data_diff_models import Comparison


def analyze_diff_rows(diff_rows, primary_keys):
    source_records = {}
    target_records = {}
    exclusive_to_target = []
    exclusive_to_source = []
    duplicates_in_source = []
    duplicates_in_target = []
    records_with_differences = []
    null_primary_keys_source = []
    null_primary_keys_target = []

    def get_key(record):
        return tuple(record.get(key) for key in primary_keys)

    for row in diff_rows:
        key = get_key(row)
        if None in key:
            if row["meta"]["origin"] == "source":
                null_primary_keys_source.append(row)
            else:
                null_primary_keys_target.append(row)
            continue

        if row["meta"]["origin"] == "source":
            if key in source_records:
                duplicates_in_source.append(row)
            else:
                source_records[key] = row
        else:  # target
            if key in target_records:
                duplicates_in_target.append(row)
            else:
                target_records[key] = row

    for key, record in target_records.items():
        if key not in source_records:
            exclusive_to_target.append(record)
        else:
            source_record = source_records[key]
            if any(
                source_record.get(k) != record.get(k)
                for k in set(source_record.keys()) | set(record.keys())
                if k != "meta"
            ):
                records_with_differences.append((source_record, record))

    for key, record in source_records.items():
        if key not in target_records:
            exclusive_to_source.append(record)

    return {
        "exclusive_pk_values_target": exclusive_to_target,
        "exclusive_pk_values_source": exclusive_to_source,
        "duplicate_pk_values_source": duplicates_in_source,
        "duplicate_pk_values_target": duplicates_in_target,
        "records_with_differences": records_with_differences,
        "null_pk_values_source": null_primary_keys_source,
        "null_pk_values_target": null_primary_keys_target,
    }


def count_duplicates_pks(diff_rows, src_pks, tgt_pks):
    source_counts = defaultdict(int)
    target_counts = defaultdict(int)

    for row in diff_rows:
        if row["meta"]["origin"] == "source":
            key = tuple(row.get(pk) for pk in src_pks)
            source_counts[key] += 1
        elif row["meta"]["origin"] == "target":
            key = tuple(row.get(pk) for pk in tgt_pks)
            target_counts[key] += 1

    source_duplicates = sum(1 for count in source_counts.values() if count > 1)
    target_duplicates = sum(1 for count in target_counts.values() if count > 1)

    return source_duplicates, target_duplicates


def generate_table_name(file_path, is_table: bool = True):
    base_name = os.path.basename(file_path)
    if is_table:
        table_name = os.path.splitext(base_name)[0]
    else:
        table_name = base_name
    return table_name


def calculate_column_differences(source_columns, target_columns, columns_mappings):
    columns_with_unmatched_data_type = []
    columns_not_compared = []

    # Create a dictionary for quick lookup of source and target columns by their names
    source_column_dict = {col["column_name"]: col for col in source_columns}
    target_column_dict = {col["column_name"]: col for col in target_columns}

    for mapping in columns_mappings:
        source_col_name = mapping["source"]
        target_col_name = mapping["target"]

        source_col = source_column_dict[source_col_name]
        target_col = target_column_dict[target_col_name]

        if (
            source_col["data_type"].lower() != target_col["data_type"].lower()
            or source_col["character_maximum_length"] != target_col["character_maximum_length"]
        ):
            columns_with_unmatched_data_type.append(
                {
                    "source": {
                        "column_name": source_col_name,
                        "data_type": source_col["data_type"],
                        "character_maximum_length": source_col["character_maximum_length"],
                    },
                    "target": {
                        "column_name": target_col_name,
                        "data_type": target_col["data_type"],
                        "character_maximum_length": target_col["character_maximum_length"],
                    },
                }
            )

    mapped_source_columns = {mapping["source"] for mapping in columns_mappings}
    mapped_target_columns = {mapping["target"] for mapping in columns_mappings}

    for source_col_name in source_column_dict:
        if source_col_name not in mapped_source_columns:
            columns_not_compared.append(
                {
                    "column_name": source_col_name,
                    "data_type": source_column_dict[source_col_name]["data_type"],
                    "origin": "source",
                }
            )

    for target_col_name in target_column_dict:
        if target_col_name not in mapped_target_columns:
            columns_not_compared.append(
                {
                    "column_name": target_col_name,
                    "data_type": target_column_dict[target_col_name]["data_type"],
                    "origin": "target",
                }
            )

    return columns_with_unmatched_data_type, columns_not_compared


def duck_db_load_csv_to_table(config: Comparison, path, is_source: bool = False) -> bool:
    dir_name = "tmp"
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name)
    csv_files = glob.glob(path)

    duck_db_file_name = f"{dir_name}/{uuid.uuid4()}.duckdb"
    for csv_file in csv_files:
        try:
            table_name = generate_table_name(csv_file)
            conn = duckdb.connect(database=duck_db_file_name, read_only=False)
            conn.execute(
                """
                    CREATE TABLE {} AS SELECT * FROM read_csv('{}', AUTO_DETECT=True, HEADER=True, UNION_BY_NAME=True);

                    """.format(
                    table_name, csv_file
                )
            )
            conn.close()
        except:
            return False
    if is_source:
        config.source.filepath = duck_db_file_name
    else:
        config.target.filepath = duck_db_file_name
    return True


def find_identical_columns(source, target):
    identical_columns = []
    for s_col in source:
        for t_col in target:
            if (
                s_col["column_name"] == t_col["column_name"]
                and s_col["data_type"] == t_col["data_type"]
                and s_col["character_maximum_length"] == t_col["character_maximum_length"]
            ):
                identical_columns.append(
                    {
                        "column_name": s_col["column_name"],
                        "data_type": s_col["data_type"],
                        "character_maximum_length": s_col["character_maximum_length"],
                    }
                )
    return identical_columns


def data_diff_config_loader(config_path):
    with open(config_path, "r") as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            print(f"Error in loading configuration file: {e} comparsion key not found")
            return None


def get_data_diff_configs(data) -> List[Comparison]:
    data_sources = {
        ds["name"]: {
            "type": ds["type"],
            "connection": ds.get("connection", {}),
            "filepath": ds.get("file_path", None),
        }
        for ds in data["data_sources"]
    }
    new_structure = []

    for comparison_name, comparison_data in data["comparisons"].items():
        source_connection = data_sources[comparison_data["source"]["data_source"]]
        target_connection = data_sources[comparison_data["target"]["data_source"]]

        source_to_target = {
            item["source_column"]: item["target_column"] for item in comparison_data.get("columns_mappings", {})
        }

        # Generate source_columns and target_columns (excluding primary keys)
        source_columns = comparison_data.get("columns", [])
        target_columns = [source_to_target.get(col, col) for col in source_columns]

        # Generate primary_keys_source and primary_keys_target
        primary_keys_source = comparison_data.get("key_columns", [])
        if len(primary_keys_source) == 0:
            raise ValueError("key_columns are required for comparison")
        primary_keys_target = [source_to_target.get(pk, pk) for pk in primary_keys_source]

        if source_connection.get("type", "") == "file":
            driver_src = "duckdb"
        else:
            driver_src = source_connection.get("type", "")
        if target_connection.get("type", "") == "file":
            driver_targ = "duckdb"
        else:
            driver_targ = target_connection.get("type", "")

        new_comparison = {
            "comparison_name": comparison_name,
            "source": {
                "host": source_connection.get("connection", {}).get("host", None),
                "port": source_connection.get("connection", {}).get("port", None),
                "account": source_connection.get("connection", {}).get("account", None),
                "warehouse": source_connection.get("connection", {}).get("warehouse", None),
                "role": source_connection.get("connection", {}).get("role", None),
                "driver": driver_src,
                "table": comparison_data.get("source", {}).get("table", None),
                "database": source_connection.get("connection", {}).get("database", None),
                "schema_name": source_connection.get("connection", {}).get("schema", None),
                "username": source_connection.get("connection", {}).get("username", None),
                "password": source_connection.get("connection", {}).get("password", None),
                "filepath": source_connection.get("filepath"),
            },
            "target": {
                "host": target_connection.get("connection", {}).get("host", None),
                "port": target_connection.get("connection", {}).get("port", None),
                "account": target_connection.get("connection", {}).get("account", None),
                "warehouse": target_connection.get("connection", {}).get("warehouse", None),
                "role": target_connection.get("connection", {}).get("role", None),
                "driver": driver_targ,
                "table": comparison_data.get("target", {}).get("table", None),
                "database": target_connection.get("connection", {}).get("database", None),
                "schema_name": target_connection.get("connection", {}).get("schema", None),
                "username": target_connection.get("connection", {}).get("username", None),
                "password": target_connection.get("connection", {}).get("password", None),
                "filepath": target_connection.get("filepath"),
            },
            "source_columns": source_columns,
            "target_columns": target_columns,
            "primary_keys_source": primary_keys_source,
            "primary_keys_target": primary_keys_target,
        }
        new_structure.append(Comparison(**new_comparison))
    return new_structure
