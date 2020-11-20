import time 
import pandas as pd
import os
from datetime import datetime

from modules.snowflake_connector import *
from modules.periscope import create_view_data, create_chart_data, simple_sql_parse
from modules.filters import view_ref_replace, filter_ref_replace

def main():

    view_results = create_view_data('./views')
    explore_results = create_chart_data('./dashboards')
    
    ctx = snowflake_connect()
    snowflake_set_parameters(ctx)

    view_reference_data = view_results

    view_results = view_ref_replace(view_results, view_reference_data)
    explore_results = filter_ref_replace(view_ref_replace(explore_results, view_reference_data))

    view_results = snowflake_execute_queries(ctx, data=view_results)
    explore_results = snowflake_execute_queries(ctx, data=explore_results)

    df_views = pd.DataFrame.from_dict(view_results)
    df_explores = pd.DataFrame.from_dict(explore_results)

    final_df = pd.concat([df_views, df_explores])
    final_df['CREATED_AT'] = generate_ts()
    
    snowflake_insert_data(ctx, final_df, table_name = "PERISCOPE_TEST_RESULTS")

    # save results from parsing dwh entities used in Periscope
    df_view_tables_list = pd.DataFrame.from_dict(simple_sql_parse(view_results, periscope_type = 'view'))
    df_explore_tables_list = pd.DataFrame.from_dict(simple_sql_parse(explore_results, periscope_type = 'dashboard'))

    tables_final_df = pd.concat([df_view_tables_list, df_explore_tables_list])
    tables_final_df['CREATED_AT'] = generate_ts()

    snowflake_insert_data(ctx, tables_final_df, table_name = "PERISCOPE_DWH_ENTITIES")

    snowflake_close_connection(ctx)

if __name__== "__main__":
  main()