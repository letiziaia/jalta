import db

# Create database connection. In an interactive setting you would provide a drop-down box of supported
# databases and show fields for all required credentials
engine = db.engine(db='snowflake',
                   user='dev_edw_junction_team_15',
                   password='BUgZhuJR4ktMrbBzv7hCV6WjH6sGYMTa',
                   account='paulig.west-europe.azure',
                   warehouse='WH01',
                   database='DEV_EDW_JUNCTION',
                   schema='JUNCTION_2020'
                   )

# Dictionary mapping each column of the database to columns used in the analysis. In an interactive setting
# you would have drop-down boxes for each required column from which you would choose the correct column in
# the database.
cols = {
    'header_bookingdate': 'date',
    'header_total': 'total'
}

# Get sales data dataframe. Constraints takes a list of tuples ('column_name', value), equal to WHERE statement in
# SQL.
df = db.sale_data(engine=engine,
                  columns=cols,
                  constraints=[('item_unit', 'kpl')])


