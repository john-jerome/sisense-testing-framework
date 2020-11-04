import re

def simple_sql_parse(data, periscope_type):
    """Using regex to parse table names from a sql query and store them in a list."""

    exp = r"\b((accounting|dim_models|raw|data_marts|base)\.\w*)\b"

    print("Extracting table names...\n")

    tables_list = []

    for row in data:

        tuple_list = re.findall(exp, row['SQL_CODE_RAW'], re.S|re.I)
        table_names_list = set(["".join(tuple[0]) for tuple in tuple_list])
        for table_name in table_names_list:
            tables_dict = {}

            tables_dict['PERISCOPE_NAME'] = row['NAME']
            tables_dict['PERISCOPE_TYPE'] = periscope_type
            tables_dict['TABLE_NAME'] = table_name

            tables_list.append(tables_dict)


    return tables_list
