import snowflake.connector
import os
import datetime
import pytz

from snowflake.connector.pandas_tools import write_pandas

account = 'yz13668.eu-central-1'
schema = 'BASE'

def generate_ts():
    """Generate current timestamp in Snowflake format."""

    tz = pytz.timezone('Europe/Berlin')
    current_ts = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    return current_ts

def snowflake_connect():
    """Connect to Snowflake warehouse with user credentials."""

    print("Connecting to the database... \n")
    try:
        ctx = snowflake.connector.connect(
            user = os.getenv("SfUser"),
            password = os.getenv("SfPassword"),
            account = account,
            schema = schema)
        print("Connected to the database. \n")
    except Exception as e:
        print("Could not connect to the database. \n")
        print(e)
        exit()
    
    return ctx

def snowflake_set_parameters(ctx, role = 'TRANSFORMER_ROLE', wh = 'TRANSFORMING_WH', db = 'ANALYTICS', schema = 'DBT_META'):
    """Set Python-Snowflake connector parameters."""
    
    cs = ctx.cursor()
    try:
        cs.execute("USE ROLE " + '"' +  role + '"')
        cs.execute("USE WAREHOUSE " + '"' +  wh + '"')
        cs.execute("USE DATABASE " + '"' +  db + '"')
        cs.execute("USE SCHEMA " + '"' +  schema + '"')
        print("Using " + role + " and " + wh + " now.\n")
    except:
        print("Cannot use " + role + " or " + wh + '.')
    
def snowflake_execute_queries(ctx, data):
    """Execute sql queries from sql_code column and store the results."""

    print("Executing the queries...\n")

    # exclude some explores from here to avoid noise in the project
    exclude_list = [
        'chart_bank_connection_performance_continuous_connection_kpi',
        'chart_platform_customer_risk_overview_rating_deterioration_to__hr__or_of_at_least_2_grades_of_customers_active_in__daterange_',
        'chart_2020_q4_okr_4_detail_customers_w__accepted_demand_test',
        'chart_flow__customer_risk_overview_rating_deterioration_to__hr__or_of_at_least_2_grades_of_customers_active_in__daterange_'
        ]

    for row in data:
        cs = ctx.cursor()
        if ('[funnel]' in row['SQL_CODE_RAW']) or any(explore in row['NAME'] for explore in exclude_list):
              row['PASS'] = 'true'
        else:
            try:
                cs.execute('SELECT * FROM(\n' + row['SQL_CODE_RAW'] + '\n) LIMIT 1')
                row['PASS'] = 'true'
            except Exception as e:
                row['PASS'] = 'false'
                row['COMPILATION_ERROR'] = str(e)
            finally:
                cs.close()

    return data


def snowflake_insert_data(ctx, df, table_name):
    """Dump data into our Snowflake DWH."""

    #success, nchunks, nrows, _ = write_pandas(ctx, df, table_name)
    try:
        _, _, nrows, _ = write_pandas(ctx, df, table_name)
        print("Successfully written " + str(nrows) + " rows of data to Snowflake.\n")
    except Exception as e:
        print("Could not save the data.\n")
        print(e)


def snowflake_close_connection(ctx):
    """Close connection to Snowflake database."""

    try:
        ctx.close()
        print("Snowflake connection has been closed. \n")
    except:
        print("Snowflake connection could not be closed. \n")