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

import json
from typing import List

from .data_differ import diff_db_tables
from .models.data_diff_models import Comparison
from .utils import data_diff_config_loader, get_data_diff_configs


def data_diff_cli(
    config_path,
    save_json: bool,
    json_path: str,
    is_cli: bool = True,
    compare: str = None,
    show_stats: bool = False,
    html_report: bool = False,
    report_path: str = "datadiff_report.html",
):
    yaml_config = data_diff_config_loader(config_path)
    comparisons: List[Comparison] = get_data_diff_configs(yaml_config)
    comp_name_found = False
    result = None
    for comparison in comparisons:
        if comparison.comparison_name == compare:
            result = diff_db_tables(comparison, is_cli, show_stats, html_report, report_path)
            total_seconds = result.get("meta", {}).get("seconds", 0)
            print(f"Time took: {total_seconds:.2f} {'seconds' if total_seconds > 1 else 'second'}")
            comp_name_found = True

    if not comp_name_found:
        raise ValueError(f"Comparison name {compare} not found in the config file")
    if save_json:
        if result is not None:
            with open(json_path, "w") as f:
                f.write(json.dumps(result, indent=3))
