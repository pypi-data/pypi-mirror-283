import sqlalchemy
from sqlalchemy.sql import text as sql_text
import pandas as pd


def sync(connection, schema, table, df, if_exists="fail", index=False, **kwargs):
    """
    ingest a single row of hard coded data into the table

    Parameters:
        schema: (str) the name of the schema where 'table' will be held
        table: (str) the name of the table to use
        df: (Pandas DataFrame) the data to be stored in the table
        if_exists: (str) argument that will be passed to the underlying
            Pandas function. See Pandas docs for DataFrame.to_sql
        index: (bool) whether to write the index of the dataframe
        **kwargs: all other key-value arguments will be passed to the
            pandas.to_sql function

    NOTE: this function will fail if the DataFrame has individual cells
    that contain complex objects (e.g. numpy arrays). In this case, it may
    be possible to convert the cells to another format (e.g. a list-of-lists,
    or a JSON object)
    """

    df.to_sql(
        table,
        con=connection,
        schema=schema,
        index=index,
        if_exists=if_exists,
        **kwargs,
    )
    
    return schema


def query(connection, sql, params=None):
    """
    Read full results set from Data Workspace based on arbitrary query

    Parameters:
        sql: a valid Postgres-SQL query
        params: a dictionary of parameters to format the SQL string
            See https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql

    Returns:
        df: pandas dataframe read from Data Workspace
    """

    return pd.read_sql(sql_text(sql), connection, params=params)