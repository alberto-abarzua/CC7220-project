from random import choice
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from shutil import rmtree
import pandas as pd
import json
import dateutil.parser
import os
from urllib.parse import quote

import sys

# Usefull functions

def get_category_name(series, key):
    return series.apply(lambda x: categories[key][x]["snippet"]["title"])


def get_publish_timestamp(series):
    return series.apply(lambda x: dateutil.parser.isoparse(x).strftime(f))


def get_trending_timestamp(series):
    return series.apply(lambda x: datetime.strptime(x, "%y.%d.%m").strftime(f))


def remove_tags(x):
    res = []
    for elem in x:
        elem  = elem.replace('"',"")
        # Replace spaces with _
        elem = elem.replace(" ","_")
        elem = quote(elem,safe='/:?=&')
        if elem in tag_set:
            res.append(elem)

    return res

if __name__ == "__main__":

    # Paremeters

    FRAC,thresh = float(sys.argv[1]),int(sys.argv[2])



    # Datos de kaggle
    RAW_DATA = Path("raw_dataset").absolute()

    # Output de datos (datos limpios)

    CLEAN_DATA = Path("clean_dataset").absolute()

    if CLEAN_DATA.exists():
        rmtree(CLEAN_DATA)
        os.mkdir(CLEAN_DATA)
    else:
        os.mkdir(CLEAN_DATA)


    # Lista de países.
    countries = ["CA", "DE", "FR", "GB", "JP", "KR", "IN", "MX", "RU", "US"]
    videos = {}  # Lista con los dataframes de archivos csv
    categories = {}  # Lista con los diccionarios de los archivos json.
    print("Abriendo archivos del dataset-->")
    for i, country in enumerate(countries):
        print(f"\tPais: {country}  {i+1}/{len(countries)} ", end="\r")
        file_csv = RAW_DATA.joinpath(f"{country}videos.csv")
        videos[country] = pd.read_csv(
            file_csv, encoding="ISO-8859-1", lineterminator="\n")
        videos[country].columns = [x.strip() for x in videos[country].columns]

        with open(RAW_DATA.joinpath(f"{country}_category_id.json")) as file:
            items = json.load(file)["items"]
            # La llave de cada categoria es su id.
            temp = {int(x["id"]): x for x in items}
            val = defaultdict(lambda: "NULL")
            val["snippet"] = defaultdict(lambda: "NULL")
            val["snippet"]["title"] = 'No categoria'
            categories[country] = defaultdict(lambda: val, temp)
    print("\nDatos Cargados!")


    f = '%Y-%m-%dT%H:%M:%S'



    for key,df in videos.items():
        df["category"] = get_category_name(df["category_id"],key) # Agregamos el nombre de la categoria
        # Parseamos las fechas para llegar y comparar como timestamps
        df["publish_timestamp"] = get_publish_timestamp(df["publish_time"]) 
        df["trending_timestamp"] = get_trending_timestamp(df["trending_date"]) 
        df.drop(["video_id","category_id","thumbnail_link"],axis =1,inplace=True)



    df_all = pd.DataFrame(columns=["country"] + list(videos["CA"].columns))
    for i, (key, df) in enumerate(videos.items()):
        df["country"] = key
        print(
            f"Escribiendo {key}videos.csv   {i+1}/{len(videos.items())}", end="\r")
        # get 10% sample of df
        # remove rows with no tags
        df = df[df["tags"] != "[none]"]
        df = df.sample(frac=FRAC)
        df_all = pd.concat([df_all, df], ignore_index=True)
    # Add numeric id to each row called video_id
    df_all["video_id"] = df_all.index


    tags_series = df_all["tags"].apply(lambda x: x.split("|"))
    tags_series = tags_series.apply(lambda x: [y.strip() for y in x])
    tags = [item for sublist in tags_series for item in sublist] # Lista con todas las tags.
    new_tags = []
    for tag in tags:
        # remove " from tags
        tag = tag.replace('"',"")
        # Replace spaces with _
        tag = tag.replace(" ","_")
        tag = quote(tag,safe='/:?=&')
        new_tags.append(tag)

    tags = new_tags


    # Count frequency of each tag
    freq_dict = {}
    for tag in tags:
        if tag in freq_dict:
            freq_dict[tag] += 1
        else:
            freq_dict[tag] = 1

    # Remove tags that appear less than 100 times


    freq_dict = {key:value for key,value in freq_dict.items() if value >= thresh}
    tag_set = freq_dict.keys()


    # Remove from every elemnt in tag series values that are not in final_set


    tags_series = tags_series.apply(remove_tags)



    # print info

    # print("\n------------BEFORE------------\n")
    # print(f"Number of unique tags : {len(set(new_tags))}")
    # print(f"Total number of tags: {len(new_tags)}")
    # print("\n------------AFTER------------\n")

    # print(f"Number of unique tags : {len(tag_set)}")
    # print("Total number of tags.",sum(freq_dict.values()))
    # print("Rows without tags {}".format(len(tags_series[tags_series.apply(lambda x: len(x) == 0)])))


    # create enw dataframe with 2 columns video_id and tag_id
    video_tag_df = pd.DataFrame(columns = ["video_id","tag_name"],index = range(sum(freq_dict.values())))
    counter = 0
    for elem in enumerate(tags_series):
        L = elem[1]
        for tag in L:
            video_tag_df.loc[counter] = [elem[0],tag]
            counter += 1
    df_all = df_all.drop(["tags","description"],axis = 1)




    # replace " " with "_"
    df_all["category"] = df_all["category"].apply(lambda x: x.replace(" ","_"))
    # remove control caracters from channel_tittle
    df_all["channel_title"] = df_all["channel_title"].apply(lambda x: x.replace(" ","_"))
    df_all["channel_title"] = df_all["channel_title"].apply(lambda x: quote(x,safe='/:?=&'))


    # Save dataframes to csv
    print("\nSaving dataframes to csv")

    # print number of elemnts in total
    num_row = df_all.shape[0] + video_tag_df.shape[0]
    print('Saving {} rows'.format(num_row))


    df_all.to_csv(CLEAN_DATA /"videos.csv",index = False)
    video_tag_df.to_csv(CLEAN_DATA /"video_tags.csv",index = False)