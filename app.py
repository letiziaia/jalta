from flask import Flask
from flask import render_template
import mimetypes
import some_plots
import json
import pandas as pd

df = pd.concat([pd.read_csv('cafe_pos_data_1.csv'), pd.read_csv('cafe_pos_data_2.csv')])
items = ['8569864530471244163', '-6433072210751770779', '3283340315810741494']
item_set = [json.dumps(some_plots.what_should_I_sell_next(df, item)) for item in items]

mimetypes.add_type('text/javascript', '.js')



app = Flask(__name__)

@app.route('/')
def main_page():
    timeseries = some_plots.get_timeseries_data(df)
    piechart = some_plots.get_piechart_data(df, 5)
    byhour = some_plots.get_data_byhour_byweekday(df)
    total_sales = int(df['HEADER_TOTAL'].sum())
    total_income = round(df['ITEM_NORMAL_PRICE'].sum(), 2)
    return render_template('index.html', timeseries=json.dumps(timeseries),
                           topproduct=json.dumps(piechart),
                           byhour=json.dumps(byhour),
                           total_sales=total_sales, total_income=total_income,
                           item_set=item_set)


if __name__ == '__main__':
    # run the app
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = False
    app.run()