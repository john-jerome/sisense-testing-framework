[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Introduction <img src="logos/sisense.png" align="right" width="200px"/>
The purpose of this tool is to introduce a testing process which allows to identify broken charts on Sisense for CDT (former Periscope Data) before actual business users encounter them.
It was developed by our BI Team at [Billie](https://www.billie.io)

## Getting Started
**Disclaimer**: since we at Billie use Snowflake as our primary cloud DWH solution, this tool is designed to work with [The Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html). However, this specific module can be replaced with any other database connector of your choice. 

The easiest way to start using this code is to add it as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to your Sisense repository:

```shell
git submodule add https://github.com/ozean12/sisense-testing-framework 
```

Next, you need to commit and push these changes:

```shell
git commit -am 'Add sisense testing module'
git push origin main
```

In order to connect the tool with your Snowflake database, you need to add a few enviromental variables which are passed to `snowflake_connect` function:

```python
ctx = snowflake.connector.connect(
              user = os.getenv("SfUser"),
              password = os.getenv("SfPassword"),
              account = os.getenv("SfAccount"),
              schema = os.getenv("SfSchema")
            )
```

If set up correctly, the framework will write data to two tables in the specified database schema. By default their names are `PERISCOPE_TEST_RESULTS` and `PERISCOPE_DWH_ENTITIES` and they need to be created in advance (you can of course choose your own names) :

```sql
CREATE OR REPLACE TABLE PERISCOPE_TEST_RESULTS (
	NAME VARCHAR(16777216),
	BI_NAME VARCHAR(16777216),
	OWNER VARCHAR(16777216),
	SQL_CODE VARCHAR(16777216),
	SQL_CODE_RAW VARCHAR(16777216),
	PASS VARCHAR(16777216),
	CREATED_AT TIMESTAMP_NTZ(9),
	COMPILATION_ERROR VARCHAR(16777216)
);

CREATE OR REPLACE TABLE PERISCOPE_DWH_ENTITIES (
	PERISCOPE_NAME VARCHAR(256),
	PERISCOPE_TYPE VARCHAR(256),
	TABLE_NAME VARCHAR(256),
	CREATED_AT TIMESTAMP_NTZ(9)
);
```


## Using the framework

After adding the submodule and setting up the database, you can run the testing framework using a deployment/runtime environement tool of your choise (e.g. Jenkins, Heroku, etc).

*Please note that you need to deploy your Sisense repo and not this one.*

Once deployed, run

```bash
git submodule update --remote sisense-testing-framework
```

to fetch and update the submodule and

```
python3 app.py
```

to run the app itself.

## TODO

* ~~Improve SQL parsing mechanism.
* Handle charts with identical names.


## Contributing
PRs and issues are welcome! 🎉

