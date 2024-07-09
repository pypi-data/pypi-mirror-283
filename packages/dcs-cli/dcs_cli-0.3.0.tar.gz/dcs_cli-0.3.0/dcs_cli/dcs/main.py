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

from typing import Any, List

from .data_differ import diff_db_tables
from .models.data_diff_models import Comparison
from .utils import data_diff_config_loader, get_data_diff_configs


class DcsSdk:
    def __init__(self, config_path: str, api_key: str = "ABC"):
        self.default_api_key = "ABC"
        self.config_path = config_path
        self.api_key = api_key
        self.__validate_api_key()
        self.data_diff_config = self.__load_data_diff_config()

    def __validate_api_key(self):
        if not self.api_key or self.api_key != self.default_api_key:
            raise ValueError("Invalid API key provided.")

    def __load_data_diff_config(self) -> dict:
        return data_diff_config_loader(self.config_path)

    def run(self):
        """
        Run Data-Diff
        """
        data_diff = None

        if self.data_diff_config is not None:
            data_diff = self.__run_data_diff()

        return data_diff

    def __run_data_diff(self) -> Any:
        """
        Run Data Diff
        """
        results = []
        comparisons: List[Comparison] = get_data_diff_configs(self.data_diff_config)
        for comparison in comparisons:
            result = diff_db_tables(comparison)
            results.append(result)
            break
        return results
