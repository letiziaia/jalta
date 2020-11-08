import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from mlxtend.frequent_patterns import apriori


def pie_chart(df, max_number=15):
    """columns needed: ITEM_CODE"""
    df['ITEM_CODE'] = df['ITEM_CODE'].astype('object')
    vc = df['ITEM_CODE'].value_counts()[:max_number].reset_index()
    fig = px.pie(vc, names='index', values='ITEM_CODE')
    # fig.show()
    return fig


def total_sales_plot(df):
    """columns: 'HEADER_ID', 'HEADER_TOTAL', 'HEADER_BOOKINGDATE', 'HEADER_JOURNALTIME'"""
    receipts = df[['HEADER_ID', 'HEADER_TOTAL', 'HEADER_BOOKINGDATE', 'HEADER_JOURNALTIME']].drop_duplicates()
    ts = receipts.groupby('HEADER_BOOKINGDATE').sum()

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=ts.index, y=ts['HEADER_TOTAL'])
    )

    # Set title
    fig.update_layout(
        title_text="Total sales per day"
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return fig

    def trend_and_season_decompose(df, model='additive'):
        """model is either additive or multiplicative;
        columns: 'HEADER_ID', 'HEADER_TOTAL', 'HEADER_BOOKINGDATE', 'HEADER_JOURNALTIME'
        """
        receipts = df[['HEADER_ID', 'HEADER_TOTAL', 'HEADER_BOOKINGDATE', 'HEADER_JOURNALTIME']].drop_duplicates()
        ts = receipts.groupby('HEADER_BOOKINGDATE').sum()
        if model == 'additive':
            result = seasonal_decompose(ts['HEADER_TOTAL'], model='additive', period=1)
            result.plot()
        else:
            result = seasonal_decompose(ts['HEADER_TOTAL'], model='multiplicative', period=1)
            result.plot()
        return

    def frequent_itemsets(df):
        """returns a pandas data frame with frequent itemsets"""
        ## dummies is needed for apriori/frequent itemsets
        dummies = pd.get_dummies(df['ITEM_CODE'])
        dummies['HEADER_ID'] = df['HEADER_ID']
        dummies = dummies.groupby('HEADER_ID').sum()
        dummies.replace({0: False}, inplace=True)
        ## TODO: regex to substitute whatever number with true
        for d in range(1, 20, 1):
            dummies.replace({d: True}, inplace=True)

        ## last line of this cell produces a table with 3 columns
        ## first col: 'support' --> those values are in the descending order, so most relevant first
        ## second col: 'itemsets' --> each element is a tuple of ITEM_CODE
        ## third col: 'length' --> how many elements in the tuple

        ap = apriori(dummies, min_support=0.1, use_colnames=True)
        ap['length'] = ap['itemsets'].apply(lambda x: len(x))
        ap = ap[ap['length'] > 1]
        return ap.sort_values('support', ascending=False)

    def what_should_I_sell_next(customer_ordered='8569864530471244163'):
        """return the list of items that are often bought together with what customer_ordered"""
        ap = frequent_itemsets(df)
        new_col = []
        # the elements in itemsets are in a weird format
        # turn each one into a list
        for i, row in ap.iterrows():
            temp = [str(e) for e in row['itemsets']]
            new_col.append(temp)
        ap['itemsets'] = new_col

        collect_suggestions = list()
        for i, row in ap.iterrows():
            if customer_ordered in row['itemsets']:
                for elm in row['itemsets']:
                    if elm not in collect_suggestions:
                        collect_suggestions.append(elm)
        return collect_suggestions.remove(customer_ordered)