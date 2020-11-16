import os
import yaml
import re

def create_view_data(start_path):
    """
    Create a list of view names and the corresponding sql queries.
    This only produces the initial data that is to be augmented later.
    """
    
    view_results = []

    print("Processing the view data...\n")

    for path, _, files in os.walk(start_path, topdown=True):
        for filename in files:
            if ".sql" in filename:
                view_dict = {}
                view_dict['NAME'] = filename.split('.')[0]

                path_sql = os.path.join(path, filename)
                with open(path_sql) as f:

                    view_dict['SQL_CODE'] = f.read()
            
                path_yaml = os.path.join(path, filename.replace(".sql", ".yaml"))
                with open(path_yaml) as f:
                    parsed_yaml_file = yaml.load(f, Loader=yaml.FullLoader)

                    view_dict["OWNER"] = parsed_yaml_file['Settings']['Metadata']['Owner'] or "No Owner"
                
                view_dict['BI_NAME'] = filename.split('.')[0]

                view_results.append(view_dict)       

    return view_results


def create_explore_data(start_path):
    """
    Create a list of chart names and the corresponding sql queries.
    This only produces the initial data that is to be augmented later.
    """

    chart_results = []

    print("Processing the charts data...\n")

    for path, _, files in os.walk(start_path):
        excluded_dashboards = [
                'wip', 
                'untitled', 
                'personal', 
                'account_optimization', 
                'team_workspace',
                'periscope_usage',
                'accounting_support_cases',
                'account_maintenance',
                'clone']
                
        for filename in files:
            if ('sql' in filename) and ('text' not in filename) and all(dashboard not in path for dashboard in excluded_dashboards):
                chart_dict = {}

                path_sql = os.path.join(path, filename)
                dashboard_with_id = path_sql.split('/')[2]
                chart_dict["NAME"] = 'chart_'  + dashboard_with_id.split('.')[0]  + '_' + filename.split('.')[0]
                
                try:
                    with open(path_sql) as f:
                        chart_dict['SQL_CODE'] = f.read()
                except Exception as e:
                    print(e)
                
                path_chart_yaml = os.path.join(path, filename.replace(".sql", ".yaml"))
                
                try:
                    with open(path_chart_yaml) as f:
                        parsed_yaml_file = yaml.load(f, Loader=yaml.FullLoader)
                        chart_name = parsed_yaml_file['display_name']
                except Exception as e:
                    print(e)

                path_dashboard_yaml = os.path.join(start_path, dashboard_with_id, dashboard_with_id.split('.')[0] + '.yaml')

                try:
                    with open(path_dashboard_yaml) as f:
                        parsed_yaml_file = yaml.load(f, Loader=yaml.FullLoader)

                        dashboard_name = parsed_yaml_file['display_name']
                        chart_dict["OWNER"] = parsed_yaml_file['dashboard_preferences']['settings']['owner'] or "No Owner"
                        chart_dict["BI_NAME"] = (dashboard_name + ": " + chart_name) or "No Name"
                except Exception as e:
                    chart_dict["OWNER"] = "No Owner"
                    chart_dict["BI_NAME"] = "No Name"
                    print(e)
    
                chart_results.append(chart_dict)

    return chart_results

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
