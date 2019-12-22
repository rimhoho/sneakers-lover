from flask import Flask, jsonify, render_template, redirect
import pymongo
from pymongo import MongoClient
import pandas as pd
from pandas.io.json import json_normalize
import os

cluster = MongoClient('mongodb+srv://rimho:0000@cluster0-yehww.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['stockX_db']
collections = [db[c] for c in ['adidas-yeezy-boost-350-v2-cloud-white', 'adidas-yeezy-500-soft-vision', 'adidas-yeezy-boost-700-inertia','air-jordan-6-retro-travis-scott','air-jordan-1-retro-high-shattered-backboard-3', 'air-jordan-11-retro-playoffs-2019']]
documents =  [collection.find() for collection in collections]
# print('WHAT!!', documents)
# print('WHAT!!', os.system("product.py"))

products = []
for document in documents:
    for p in document:
        products.append(p)
table = json_normalize(products, max_level=1)

app = Flask(__name__)

@app.route('/')
def home():  
    columns_name = list(table)
    basic_df = table.drop(table.columns[[0, 2, 6, 10]], axis=1)
    cols = basic_df.columns.tolist()
    cols = cols[:2] + cols[3:5] + [cols[2]] + cols[5:]
    df_release_date = basic_df[cols].sort_values(by='release_date', ascending=False)
    return render_template("index.html", dataset = df_release_date)


@app.route('/api')
def api():
    data = []
    each_data = {}
    history = table['sale_history']
    name,date,time,size,price = [],[],[],[],[]
    for sneaker in history:
        for value in sneaker:
            name.append(value['name'])
            date.append(value['date'])
            time.append(value['time'])
            size.append(value['size'])
            price.append(value['price'])
    df = pd.DataFrame({'name': name, 'date': date, 'time': time, 'size': size, 'price': price})
    df = df.replace(to_replace ='[\$,]', value = '', regex = True)
    df = df.astype({'size': 'float', 'price': 'int'})
    df['index'] = df.index
    df['category'] = df['name'].str.split("-", expand = True)[1]
    df['days'] = df['date'].str.split(" ", n = 1, expand = True)[0]
    df['am/pm'] = df['time'].str.split(" ", n = 2, expand = True)[1]

    df_name_trend = df.groupby( df['name']).agg( max_price=('price', 'max'), min_price=('price', 'min'), count_sneakers=('index', 'count'))
    # df_name_trend['name'] = df_name_trend.index
    each_data['Overall Sales on StockX for about a month'] = df_name_trend.to_dict()

    df_size_trend = df.groupby([df['category'], df['size']]).agg( max_price=('price', 'max'), count_sneakers=('index', 'count'))
    df_size_trend['size']= df_size_trend.index.get_level_values('size')
    df_size_trend.sort_values('max_price', ascending = False)
    size_trend = {}
    for dicts in df_size_trend.to_dict():
        new_data = []
        for key, value in zip(df_size_trend.to_dict()[dicts].keys(), df_size_trend.to_dict()[dicts].values()):
            new_dic = {}
            new_dic[str(value)] = list(key)
            new_data.append(new_dic)
        size_trend[dicts] = new_data
    each_data['What size and which brand are more profitable'] = size_trend

    df2 = df.loc[df['size'] == 7.5]
    df_7half_size_trend = df2.groupby(df['name']).agg(avg_price=('price', 'mean'), count_sneakers=('index', 'count'), size=('size', 'mean'))#, retaile_price=('retaile_price', 'mean'))
    df_7half_size_trend['retaile_price'] = [200, 220, 300, 160, 220, 250]
    df_7half_size_trend['how_much_earn'] = [((a-b)/b)*100 for a,b in zip(df_7half_size_trend['avg_price'], df_7half_size_trend['retaile_price'])]
    each_data['More details of the size 7.5'] = df_7half_size_trend.to_dict()
 
    df_time_trend = df.groupby([df['am/pm'], df['days']]).agg( max_price=('price', 'max'), min_price=('price', 'min'), avg_price=('price', 'mean'))
    df_time_trend['avg_price'] = ['{:05.2f}'.format(a) for a in df_time_trend['avg_price']]
    time_trend = {}
    for dicts in df_time_trend.to_dict():
        new_data = []
        for key, value in zip(df_time_trend.to_dict()[dicts].keys(), df_time_trend.to_dict()[dicts].values()):
            new_dic = {}
            new_dic[str(value)] = list(key)
            new_data.append(new_dic)
        time_trend[dicts] = new_data
    each_data['Best time to buy/sell Sneakers'] = time_trend

    data.append(each_data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)




