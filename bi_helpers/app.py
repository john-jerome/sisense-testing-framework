import time 
import pandas as pd
import os

from datetime import datetime

from modules.sqlparse import simple_sql_parse
from modules.snowflake_connector import snowflake_connect, snowflake_execute_queries, snowflake_close_connection, snowflake_set_parameters, snowflake_dump_table, generate_ts
from modules.periscope import create_view_data, create_explore_data
from modules.filter import view_ref_replace, filter_ref_replace

if __name__== "__main__":

    # generate current timestamp

    generated_at = generate_ts()

    view_start_path = './views' # current views directory
    dashboard_start_path = './dashboards' # current dashboards dictionary

    view_results = create_view_data(view_start_path)
    explore_results = create_explore_data(dashboard_start_path)
    
    view_reference_data = view_results

    ctx = snowflake_connect()
    snowflake_set_parameters(ctx)

    view_results = view_ref_replace(view_results, view_reference_data)
    explore_results = view_ref_replace(explore_results, view_reference_data)

    explore_results = filter_ref_replace(explore_results)

    view_results = snowflake_execute_queries(ctx, view_results)
    explore_results = snowflake_execute_queries(ctx, explore_results)

    df_views = pd.DataFrame.from_dict(view_results)
    df_explores = pd.DataFrame.from_dict(explore_results)

    final_df = pd.concat([df_views, df_explores])
    final_df['CREATED_AT'] = generated_at
    
    snowflake_dump_table(ctx, final_df)

    # save results from parsing tables used in Periscope
    view_tables_list = simple_sql_parse(view_results, periscope_type = 'view')
    explore_tables_list = simple_sql_parse(explore_results, periscope_type = 'dashboard')

    df_view_tables_list = pd.DataFrame.from_dict(view_tables_list)
    df_explore_tables_list = pd.DataFrame.from_dict(explore_tables_list)

    tables_final_df = pd.concat([df_view_tables_list, df_explore_tables_list])
    tables_final_df['CREATED_AT'] = generated_at

    snowflake_dump_table(ctx, tables_final_df, table_name = "PERISCOPE_DWH_ENTITIES")

    snowflake_close_connection(ctx)
