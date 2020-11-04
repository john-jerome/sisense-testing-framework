import os

def create_view_data(start_path):
    """
    Create a list of view names and the corresponding sql queries.
    This only produces the initial data that is to be augmented later.
    """
    
    view_results = []

    print("Processing the view data...\n")

    for path,dirs,files in os.walk(start_path):
        for filename in files:
            if ".sql" in filename:
                full_path = os.path.join(path,filename)
                with open(full_path) as f:
                    view_dict = {}

                    # view name without id/hash
                    view_name = filename.split('.')[0]
                    view_dict['NAME'] = view_name
                    view_dict['SQL_CODE'] = f.read()
                    view_results.append(view_dict)

    return view_results


def create_explore_data(start_path):
    """
    Create a list of explore names and the corresponding sql queries.
    This only produces the initial data that is to be augmented later.
    """
    explore_results = []

    print("Processing the explore data...\n")

    for path,dirs,files in os.walk(start_path):
        excluded_dashboards = [
                'wip', 
                'untitled', 
                'personal', 
                'account_optimization', 
                'team_workspace',
                'periscope_usage',
                'accounting_support_cases',
                'account_maintenance']
                
        for filename in files:
            if ('sql' in filename) and ('text' not in filename) and all(dashboard not in path for dashboard in excluded_dashboards):
                full_path = os.path.join(path,filename)
                with open(full_path) as f:
                    explore_dict = {}

                    # compiling a readable explore name
                    explore_name = full_path.split('/')[1] + '_'  + (full_path.split('/')[2]).split('.')[0] + '_' + filename.split('.')[0]
                    explore_dict['NAME'] = explore_name
                    explore_dict['SQL_CODE'] = f.read()
                    explore_results.append(explore_dict)

    return explore_results


