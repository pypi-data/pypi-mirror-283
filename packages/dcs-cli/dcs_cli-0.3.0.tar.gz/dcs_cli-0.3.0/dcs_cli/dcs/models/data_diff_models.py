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

from typing import List, Optional

from pydantic import BaseModel


class SourceTargetConnection(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = None
    driver: str
    table: Optional[str] = None
    database: Optional[str] = None
    filepath: Optional[str] = None
    schema_name: Optional[str] = None
    warehouse: Optional[str] = None
    role: Optional[str] = None
    account: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class Comparison(BaseModel):
    comparison_name: str
    source: SourceTargetConnection
    target: SourceTargetConnection
    source_columns: List[str]
    target_columns: List[str]
    primary_keys_source: List[str]
    primary_keys_target: List[str]
