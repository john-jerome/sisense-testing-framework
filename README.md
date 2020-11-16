[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Introduction <img src="logos/sisense.png" align="right" width="200px"/>
The purpose of this tool is to introduce a testing process which allows to identify broken charts on Sisense before actual business users encounter them.
It was developed by our BI Team at [Billie](https://www.billie.io)

## Getting Started
Disclaimer: since we at Billie use Snowflake as our primary cloud DWH solution, this tool is designed to work with [The Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html). However, this specific module can be replaced with any other database connector of your choice. 

The easiest way to start using this code is to add it as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to your Sisense for CDT (former Periscope Data) repository:

```shell
git submodule add https://github.com/ozean12/sisense-testing-framework 
```

Next, you need to commit and push these changes:

```shell
git commit -am 'Add sisense testing module'
git push origin main
```

In order to connect the tool with your Snowflake database, you need to add a few enviromental variables which are used in `snowflake_connect` function:

```python
ctx = snowflake.connector.connect(
              user = os.getenv("SfUser"),
              password = os.getenv("SfPassword"),
              account = os.getenv("SfAccount"),
              schema = os.getenv("SfSchema")
            )
```

## Using the framework

## Contributing
PRs and issues are welcome! 🎉

