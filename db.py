from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
from functools import reduce


def engine(db='snowflake', **kwargs):
    """
    Return sqlalchemy engine for a particular database
    """

    try:
        if db == 'snowflake':
            return create_engine(URL(
                account=kwargs['account'],
                user=kwargs['user'],
                password=kwargs['password'],
                database=kwargs['database'],
                schema=kwargs['schema'],
                warehouse=kwargs['warehouse']
            ))

        # Add support for other databases here

        else:
            raise ValueError('Unsupported Database')

    except KeyError as err:
        raise KeyError(f'Database of type "{db}" requires parameter {err}')


def sale_data(engine, table_name, columns, constraints=None):
    """
    Return sale data from given table
    """

    columns_inv = {v: k for k,v in columns.items()}

    df = pd.read_sql_table(
        table_name,
        con=engine,
        columns=columns.keys(),
        parse_dates=[
            columns_inv['date']
        ]
    )

    if constraints is None:
        return df

    if len(constraints) == 1:
        df = df[df[constraints[0]] == constraints[1]]
    else:
        df = df[reduce(lambda x, y: x & y, [df[attr] == val for attr, val in constraints])]

    return df.rename(columns=columns)
