# This is a sample Python script.
import json
import math
import re

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time, timedelta
import os.path, time
from dateutil import parser
import numpy as np
from dateutil.relativedelta import relativedelta
import seaborn

days = []
current = datetime(2023,12,1,5,0,0)
while current <= datetime.today():
    days.append(current)
    current += relativedelta(days=1)

DAY = len(days)

def API_call():
    url = "https://adventofcode.com/2023/leaderboard/private/view/1804979.json"
    response = requests.get(url,cookies={'session': '53616c7465645f5fc85b715077798eed379a894bfe8b5599631c8a6db1fa440b3ebd875f96491f1df2013783616d2a61b5f88a2b446dd880e9d5ababa05080ab;'})
    print(response.text)
    return response.text


def parse_json(json_data):
    data = json.loads(json_data)
    urk = [ {'member_id': key } | values for key,values in data.get("members").items() ]
    df = pd.DataFrame.from_records(urk)

    expanded_df = pd.json_normalize(df['completion_day_level'])
    result_df = pd.concat([df, expanded_df], axis=1)
    result_df = result_df.drop('completion_day_level', axis=1)
    result_df = result_df.sort_values('stars', ascending=False)
    return result_df


def fix_datetime(result_df):
    cs = result_df.columns.str.match(r'\d+.\d+.get_star_ts')
    result_df.loc[:, cs] = result_df.loc[:, cs].apply(pd.to_datetime, unit= 's')
    return result_df

def plot_star_count(result_df):
    plt.title('Star Count')
    plt.xticks(rotation=90)
    plt.grid()
    plt.bar(range(len(result_df['name'])), result_df['stars'].tolist(), tick_label=result_df['name'].tolist())
    plt.show()
def time_diff(result_df):
    for i in range(1, DAY+1):
        result_df['time_difference.'+ str(i)] = result_df.apply(lambda x: (x[str(i) + '.2.get_star_ts'] - x[str(i) + '.1.get_star_ts']).total_seconds()/60.0/60, axis=1)



def plot_first_sec_stars(result_df):
    for i in range(1, DAY+1):
        plt.clf()
        plt.xticks(rotation=90)
        plt.grid()
        plt.yticks(np.arange(0, 200 + 1, 1))
        for idx, row in result_df.iterrows():
            a = (row[str(i) + '.1.get_star_ts'].to_pydatetime() - days[i-1]).total_seconds()
            b = ( (row[str(i) + '.2.get_star_ts'].to_pydatetime() - days[i-1]).total_seconds())
            if math.isnan(a) or math.isnan(b):
                continue

            plt.title('First and Second Stars ' + str(i) + ' (in hours)')
            plt.scatter(row['name'], (row[str(i) + '.1.get_star_ts'].to_pydatetime() - days[i-1]).total_seconds()/60.0/60, color = 'grey')
            plt.scatter(row['name'], (row[str(i) + '.2.get_star_ts'].to_pydatetime() - days[i-1]).total_seconds()/60.0/60, color = 'gold')
        plt.show()

def plot_time_between_stars(result_df):
    time_diff(result_df)
    for i in range(1, DAY+1):
        plt.clf()
        plt.title('Time between stars ' + str(i) + ' (in hours)')
        plt.xticks(rotation=90)
        plt.grid()
        plt.scatter(result_df['name'], result_df['time_difference.'+ str(i)])
        plt.show()

def cache():
    if parser.parse(time.ctime(os.path.getmtime('input.txt'))) < (datetime.now() - timedelta(minutes=15)):
        print('call')
        json_data = API_call()
        with open('input.txt', 'w') as f:
            json.dump(json_data, f)
    else:
        print('load cache')
        with open('input.txt') as f:
            json_data = json.load(f)
    return json_data


def search(result_df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(result_df.loc[result_df['name'] == 'Mohamed Abukar'])


def time_people_df(result_df):
    cols = [col for col in result_df.columns if col.startswith("time_difference")]
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        df = result_df[['name'] + cols]
        print(df)
def analyse():
    json_data = cache()
    result_df = parse_json(json_data)
    result_df = fix_datetime(result_df)
    plt.clf()
    plot_star_count(result_df)
    plt.clf()
    plot_time_between_stars(result_df)
    plt.clf()
    plot_first_sec_stars(result_df)
    time_people_df(result_df)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    analyse()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
