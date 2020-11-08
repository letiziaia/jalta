import pandas as pd
import numpy as np

import plotly.express as px


def emoji_plot():
    df = pd.read_csv("igdata.tsv", index_col=0, sep="\t").reset_index().sort_values('Timestamp')
    # cut the timestamp, save day only
    df['Timestamp'] = [str(e).split(" ")[0] for e in df['Timestamp']]

    # here split emojies into single char
    all_emoji = []
    for e in df['Emojies'].dropna().values:
        for i in e:
            all_emoji.append(i)

    time = []
    lan = []
    emo = []
    for i, row in df.iterrows():
        emostr = row['Emojies']
        # print(emostr)
        # print(type(emostr))
        if emostr is not np.nan:
            for e in emostr:
                time.append(row['Timestamp'])
                lan.append(row['Language'])
                emo.append(e)

    # time, language and single emoji
    clean = pd.DataFrame({'Timestamp': time, 'Language': lan, 'Emojies': emo})

    # time, emoji, and count (under language column)
    counted = clean.groupby(['Timestamp', 'Emojies']).count().reset_index()

    emolist = counted['Emojies'].unique()

    # random scatter
    x = np.random.uniform(low=-10.0, high=10.0, size=len(emolist))
    y = np.random.uniform(low=-10.0, high=10.0, size=len(emolist))

    coords = pd.DataFrame({'Emojies': emolist, 'x': x, 'y': y})

    coords = pd.concat([counted, coords], axis=1, join='inner')

    fig = px.scatter(coords, x=x, y=y, animation_frame="Timestamp", text=coords["Emojies"].values[:, 0],
                     size=50 * coords["Language"], hover_name=coords["Emojies"].values[:, 0],
                     log_x=False, size_max=55,
                     range_x=[coords['x'].min() - 2, coords['x'].max() + 2],
                     range_y=[coords['y'].min() - 2, coords['y'].max() + 2],
                     labels={"x": "", "y": ""})
    fig.update_traces(textposition='middle center', textfont_size=10 * coords["Language"])
    fig["layout"].pop("updatemenus")

    return fig.write_html("emoji_plot.html")

emoji_plot()
