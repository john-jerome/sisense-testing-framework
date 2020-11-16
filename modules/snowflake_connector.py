import snowflake.connector
import os
import datetime
import pytz

from snowflake.connector.pandas_tools import write_pandas

def generate_ts():
    """Generate current local timestamp.

    Returns:
        current_ts (str): current timestamp converted to string.
    """

    tz = pytz.timezone('Europe/Berlin')
    current_ts = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    return current_ts

def snowflake_connect():
    """Establish Snowflake connection.

    Returns:
        ctx: database connection object
    """

    print("Connecting to the database... \n")
    try:
        ctx = snowflake.connector.connect(
            user = os.getenv("SfUser"),
            password = os.getenv("SfPassword"),
            account = os.getenv("SfAccount"),
            schema = os.getenv("SfSchema"))
        print("Connected to the database. \n")
    except Exception as e:
        print("Could not connect to the database. \n")
        print(e)
        exit()
    
    return ctx

def snowflake_set_parameters(ctx, role, wh, db, schema):
    """Set warehouse parameters.

    Args:
        ctx : database connection object
        role (str): Snowflake role
        wh (str): Snowflake warehouse
        db (str): Snowflake database
        schema (str): Snowflake schema
    """
    
    cs = ctx.cursor()
    try:
        cs.execute("USE ROLE " + '"' +  role + '"')
        cs.execute("USE WAREHOUSE " + '"' +  wh + '"')
        cs.execute("USE DATABASE " + '"' +  db + '"')
        cs.execute("USE SCHEMA " + '"' +  schema + '"')
        print("Using " + role + " and " + wh + " now.\n")
    except:
        print("Cannot use " + role + " or " + wh + '.')

def snowflake_execute_queries(ctx, data, excluded_charts=[]):
    """Run SQL queries using the Snowflake connector and store the results.

    Args:
        ctx: database connection object
        data (array of dicts): initial testing data
        excluded_charts (list): list of views/charts to exclude from testing. Default is empty list

    Returns:
        data (array of dict): testing data augmented with 'PASS' and 'COMPILATION_ERROR' columns
    """

    print("Executing the queries...\n")

    for row in data:
        cs = ctx.cursor()
        if ('[funnel]' in row['SQL_CODE_RAW']) or any(explore in row['NAME'] for explore in excluded_charts):
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
    """Write data to Snowflake.

    Args:
        ctx: database connection object
        df (pandas df): data to insert
        table_name (str): destination table name
    """
    
    try:
        _, _, nrows, _ = write_pandas(ctx, df, table_name)
        print("Successfully written " + str(nrows) + " rows of data to Snowflake.\n")
    except Exception as e:
        print("Could not save the data.\n")
        print(e)

def snowflake_close_connection(ctx):
    """Close connection to Snowflake database.

    Args:
        ctx: database connection object
    """
    
    try:
        ctx.close()
        print("Snowflake connection has been closed. \n")
    except:
        print("Snowflake connection could not be closed. \n")