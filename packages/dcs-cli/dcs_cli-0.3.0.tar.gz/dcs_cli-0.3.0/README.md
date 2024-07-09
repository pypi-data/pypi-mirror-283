<h1 align="center">
  DCS CLI v0.3.0
</h1>

> SDK for DataChecks


### Installation

> Python version `>=3.9,<3.12`

```bash

$ pip install dcs_cli[all-dbs]

```

### Example Command [CLI]

```sh

$ dcs_cli --help

$ dcs_cli run -C example.yaml --compare comparison_one --stats -j -jp output.json --html-report --report-path result.html
```
### Example Configuration

```yml

data_sources:
  - name: iris_snowflake
    type: snowflake
    connection:
      account: bp54281.central-india.azure
      username: username
      password: password
      database: TEST_DCS
      schema: PUBLIC
      warehouse: compute_wh
      role: accountadmin

  - name: pgsql
    type: postgres
    connection:
      host: localhost
      port: 5432
      username: postgres
      password: password
      database: dvdrental

  - name: file1
    type: file
    file_path: "nk.kyc_data/SOURCE_EMPLOYEE_FILE.csv"

  - name: file2
    type: file
    file_path: "nk.kyc_data/RAW_EMPLOYEE.csv"

comparisons:
  # FLATFILE TO SNOWFLAKE
  comparison_one:
    source:
      data_source: file1
      table: SOURCE_EMPLOYEE_FILE
    target:
      data_source: iris_snowflake
      table: RAW_EMPLOYEE
    key_columns:
      - custid
    columns:
      - FIRSTNAME
      - lastname
      - designation
      - salary
    columns_mappings:
      - source_column: custid
        target_column: CUSTID

      - source_column: lastname
        target_column: LASTNAME

      - source_column: designation
        target_column: DESIGNATION

      - source_column: salary
        target_column: SALARY

  # DB TO DB (SNOWFLAKE)
  comparison_two:
    source:
      data_source: iris_snowflake
      table: RAW_EMPLOYEE

    target:
      data_source: iris_snowflake
      table: TL_EMPLOYEE
    key_columns:
      - CUSTID
    columns:
      - FIRSTNAME
      - LASTNAME
      - DESIGNATION
      - SALARY

  # FILE TO FILE
  comparison_three:
    source:
      data_source: file2
      table: RAW_EMPLOYEE

    target:
      data_source: file1
      table: SOURCE_EMPLOYEE_FILE
    key_columns:
      - custid
    columns:
      - FIRSTNAME
      - lastname
      - designation
      - salary
    columns_mappings:
      - source_column: FIRSTNAME
        target_column: firstname

  # DB TO DB (Postgres)
  comparison_four:
    source:
      data_source: pgsql_1
      table: actor
    target:
      data_source: pgsql_2
      table: actor2
    key_columns:
      - actor_id
    columns:
      - first_name
      - last_name
      - last_update
    columns_mappings:
      - source_column: actor_id
        target_column: actor_id1

      - source_column: first_name
        target_column: first_name1

      - source_column: last_name
        target_column: last_name1

      - source_column: last_update
        target_column: last_update1

  # DB TO DB (Postgres)
  comparison_five:
    source:
      data_source: pgsql_1
      table: actor
    target:
      data_source: pgsql_2
      table: new_table
    key_columns:
      - actor_id
    columns:
      - first_name
      - last_name
      - last_update


Please refer to example.yaml file

```