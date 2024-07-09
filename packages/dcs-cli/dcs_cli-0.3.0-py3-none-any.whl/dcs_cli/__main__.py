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

from typing import Union

import click

from dcs_cli.__version__ import __version__
from dcs_cli.dcs.cli import data_diff_cli


@click.version_option(
    package_name="DCS CLI",
    prog_name="DCS CLI",
)
@click.group(help=f"DCS CLI version {__version__}")
def main():
    pass


@main.command(
    short_help="Starts DCS CLI",
)
@click.option(
    "-C",
    "--config-path",
    required=True,
    default=None,
    help="Specify the file path for configuration",
)
@click.option(
    "--save-json",
    "-j",
    is_flag=True,
    help="Save data into JSON file",
)
@click.option(
    "--json-path",
    "-jp",
    required=False,
    default="data_diff_report.json",
    help="Specify the file path for JSON file",
)
@click.option(
    "--compare",
    required=True,
    help="Run only specific comparisons by providing comma separated comparison names",
)
@click.option(
    "--stats",
    is_flag=True,
    help="Print stats about the data diff",
)
@click.option(
    "--html-report",
    is_flag=True,
    help="Specify if the inspection should generate HTML report",
)
@click.option(
    "--report-path",
    required=False,
    default="datadiff_report.html",
    help="Specify the file path for HTML report",
)
def run(
    config_path: Union[str, None],
    save_json: bool = False,
    json_path: str = "data_diff_report.json",
    compare: str = None,
    stats: bool = False,
    html_report: bool = False,
    report_path: str = "datadiff_report.html",
):
    if compare is None:
        raise click.BadParameter("Please provide comparison names to run")
    data_diff_cli(
        config_path,
        save_json,
        json_path,
        is_cli=True,
        compare=compare,
        show_stats=stats,
        html_report=html_report,
        report_path=report_path,
    )


if __name__ == "__main__":
    main()
