## Introduction
The purpose of this tool is to introduce a testing process which allows to identify broken charts on Sisense before actual users encounter them.
It was developed by our BI Team at [Billie](https://www.billie.io/).
![](https://github.com/ozean12/sisense-testing-framework/blob/main/logos/billie.png "Billie")
## Getting Started
Disclaimer: since we at Billie use Snowflake as our primary cloud DWH solution, this tool is designed to work with [The Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html). However, this specific module can be replaced with any other database connector of your choice. 

The easiest way to start using this code is to add it as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to your Sisense for CDT (former Periscope Data) repository:

```shell
git submodule add https://github.com/ozean12/sisense-testing-framework 
```

Next, you need to commit and push these changes:

```shell
git commit -am 'Add sisense-testing module'
git push origin main
```

## Contributing
PRs and issues are welcome! 🎉

