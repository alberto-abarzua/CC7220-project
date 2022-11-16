# CC7220-project

## Data used

- [Trending YouTube Video Statistics](https://www.kaggle.com/datasets/datasnaek/youtube-new). The data should be placed in a folder named `raw_dataset`

## Project structure

- `pre_processing.py`: Notebook to process the raw dataset downloaded from Kaggle. Running this script creates a directory named `clean_dataset`, which contains the cleaned `.csv` files. The script takes two arguments: `frac` and `threshold`. `frac` represents what fraction of the dataset to take from the raw data, and `threshold` will remove videos with less than `threshold` tags.

- `create_rdf.py`: Reads the cleaned data and uses Tarql to convert the `.csv` files into RDF triples. The `CONSTRUCT` queries in SPARQL are placed in the `sparql` folder. Running this script will create `.ttl` files. The script will place the `.ttl` files into the `rdf_dataset` directory. The `.ttl` files can now be loaded into a SPARQL endpoint to run queries.

## Prefixes

```sql
PREFIX tag: <http://www.holygoat.co.uk/owl/redwood/0.1/tags/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ex: <http://ex.org/>
PREFIX ct: <http://ex.org/country/>
PREFIX tg: <http://ex.org/tag/>
PREFIX cat: <http://ex.org/category/>
PREFIX ch: <http://ex.org/channel/>
```


## Queries

## 1. Get the average views by country:

```SPARQL
SELECT ?country (AVG(?views) as ?avg) WHERE {
  ?country a ex:Country .
  ?video a ex:Video .
  ?video ex:country ?country .
  ?video ex:views ?views
} GROUP BY(?country)
ORDER BY DESC(?avg)
```

### Results:

|      | country                    | avg                                                          |
| ---- | -------------------------- | ------------------------------------------------------------ |
| 1    | <http://ex.org/country/GB> | "6105793.23950035224624722267382"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 2    | <http://ex.org/country/US> | "2394536.7338001725275282894403"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 3    | <http://ex.org/country/CA> | "1177444.463009143807148794679967"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 4    | <http://ex.org/country/IN> | "1081487.720469266909454838619999"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 5    | <http://ex.org/country/DE> | "622963.930254701261604379909545"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 6    | <http://ex.org/country/KR> | "478380.517857142857142857142857"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 7    | <http://ex.org/country/FR> | "453443.666403162055335968379447"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 8    | <http://ex.org/country/MX> | "390053.163736800341817737899042"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 9    | <http://ex.org/country/JP> | "272906.586734399353460716965884"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 10   | <http://ex.org/country/RU> | "249568.381662358862739763297511"^^<http://www.w3.org/2001/XMLSchema#decimal> |

## 2. Highest and lowest viewcount for each channel

```SPARQL
SELECT ?channel (MIN(?views) as ?min_video) (MAX(?views) as ?max_video) WHERE{
  ?channel a ex:Channel . 
  ?video ex:channel_title ?channel .
  ?video ex:views ?views .
  ?video a ex:Video .
} GROUP BY ?channel HAVING(COUNT(*)>10)
ORDER BY DESC(?min_video) 
LIMIT 10
```



### Results:

|      | channel                                      | min_video                                              | max_video                                               |
| ---- | -------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------- |
| 10   | <http://ex.org/channel/HAITHAM_XD>           | "12118553"^^<http://www.w3.org/2001/XMLSchema#integer> | "12118553"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 9    | <http://ex.org/channel/RITIKHA_MUSIC_TRACK>  | "12229386"^^<http://www.w3.org/2001/XMLSchema#integer> | "12229386"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 6    | <http://ex.org/channel/BalajiMotionPictures> | "12672730"^^<http://www.w3.org/2001/XMLSchema#integer> | "19063679"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 7    | <http://ex.org/channel/Risingsunrsf>         | "12552714"^^<http://www.w3.org/2001/XMLSchema#integer> | "19234147"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 8    | <http://ex.org/channel/Sofia_Reyes>          | "12305311"^^<http://www.w3.org/2001/XMLSchema#integer> | "31371692"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 5    | <http://ex.org/channel/Flow_La_Movie>        | "16991901"^^<http://www.w3.org/2001/XMLSchema#integer> | "337621571"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 1    | <http://ex.org/channel/Republic_Records>     | "24412837"^^<http://www.w3.org/2001/XMLSchema#integer> | "35463645"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 4    | <http://ex.org/channel/EllaMaiVEVO>          | "18825555"^^<http://www.w3.org/2001/XMLSchema#integer> | "49178073"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 3    | <http://ex.org/channel/Lucas_Lucco>          | "19878085"^^<http://www.w3.org/2001/XMLSchema#integer> | "54087829"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 2    | <http://ex.org/channel/Kylie_Jenner>         | "20921796"^^<http://www.w3.org/2001/XMLSchema#integer> | "62338362"^^<http://www.w3.org/2001/XMLSchema#integer>  |



## 3. Get the most common tag for every category.


```sql
SELECT ?category ?tag ?cnt WHERE {
    {SELECT DISTINCT ?category (MAX(?cnt) as ?MaxCount) WHERE {
      {SELECT DISTINCT ?category ?tag (COUNT(?tag) as ?cnt) WHERE {
        ?category a ex:Category .
        ?video ex:category ?category .
        ?video ex:hasTag ?tag
      }
      GROUP BY ?category ?tag
      ORDER BY DESC(?cnt)}

    } GROUP BY ?category
    ORDER BY DESC(?MaxCount)}
  
    {SELECT DISTINCT ?category ?tag (COUNT(?tag) as ?cnt) WHERE {
        ?category a ex:Category .
        ?video ex:category ?category .
        ?video ex:hasTag ?tag
      }
      GROUP BY ?category ?tag
      ORDER BY DESC(?cnt)}


FILTER(?cnt = ?MaxCount)

}
```

### Results:

| 1    | <http://ex.org/category/Entertainment>         | <http://ex.org/tag/funny>                                    | "6222"^^<http://www.w3.org/2001/XMLSchema#integer> |
| ---- | ---------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| 2    | <http://ex.org/category/Comedy>                | <http://ex.org/tag/comedy>                                   | "4832"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 3    | <http://ex.org/category/Music>                 | <http://ex.org/tag/Pop>                                      | "3901"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 4    | <http://ex.org/category/News_&_Politics>       | <http://ex.org/tag/news>                                     | "3175"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 5    | <http://ex.org/category/Sports>                | <http://ex.org/tag/football>                                 | "2180"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 6    | <http://ex.org/category/Howto_&_Style>         | <http://ex.org/tag/how_to>                                   | "1844"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 7    | <http://ex.org/category/People_&_Blogs>        | <http://ex.org/tag/funny>                                    | "1298"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 8    | <http://ex.org/category/Film_&_Animation>      | <http://ex.org/tag/Trailer>                                  | "1260"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 9    | <http://ex.org/category/Pets_&_Animals>        | <http://ex.org/tag/cat>                                      | "1073"^^<http://www.w3.org/2001/XMLSchema#integer> |
| 10   | <http://ex.org/category/Gaming>                | <http://ex.org/tag/gameplay>                                 | "973"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 11   | <http://ex.org/category/Education>             | <http://ex.org/tag/science>                                  | "924"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 12   | <http://ex.org/category/Science_&_Technology>  | <http://ex.org/tag/unboxing>                                 | "634"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 13   | <http://ex.org/category/Autos_&_Vehicles>      | <[http://ex.org/tag/%C3%90%C2%B0%C3%90%C2%B2%C3%91%C2%82%C3%90%C2%BE](http://ex.org/tag/Ð°Ð²ÑÐ¾)> | "373"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 15   | <http://ex.org/category/Shows>                 | <http://ex.org/tag/periyamanaval>                            | "270"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 19   | <http://ex.org/category/Travel_&_Events>       | <http://ex.org/tag/food>                                     | "246"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 20   | <http://ex.org/category/No_categoria>          | <[http://ex.org/tag/%C3%90%C2%BF%C3%91%C2%83%C3%91%C2%82%C3%90%C2%B8%C3%90%C2%BD](http://ex.org/tag/Ð¿ÑÑÐ¸Ð½)> | "224"^^<http://www.w3.org/2001/XMLSchema#integer>  |
| 21   | <http://ex.org/category/Movies>                | <http://ex.org/tag/full_movie>                               | "25"^^<http://www.w3.org/2001/XMLSchema#integer>   |
| 22   | <http://ex.org/category/Nonprofits_&_Activism> | <http://ex.org/tag/feminism>                                 | "9"^^<http://www.w3.org/2001/XMLSchema#integer>    |

## 4. Find the channels with at least 15 videos or categories that have fastest time for a video to become trending (time_to_trending = trending_date - publish_date).


```sql
## Query for categories
SELECT ?category ?time_to_trending_average_hours WHERE{
{SELECT ?category (AVG(?time_in_seconds) as ?average_time_to_trending_seconds) WHERE {
  
  ?video a ex:Video .
  ?video ex:category ?category .
  ?video ex:title ?title .
  ?video ex:publish_timestamp ?publish_timestamp .
  ?video ex:trending_timestamp ?trending_timestamp
  BIND(xsd:dateTime(?trending_timestamp) - xsd:dateTime(?publish_timestamp) AS ?time2trending)       
  BIND(day(?time2trending) AS ?days)    
  BIND(hours(?time2trending) AS ?hours)   
  BIND(minutes(?time2trending) AS ?minutes)   
  BIND(seconds(?time2trending) AS ?seconds)   
  
  BIND( (?days*86400 + ?hours*3600 + ?minutes*60 + ?seconds) AS ?time_in_seconds)
  
}GROUP BY ?category}

BIND(ceil(?average_time_to_trending_seconds/3600) AS ?time_to_trending_average_hours)

}ORDER BY ASC(?time_to_trending_average_hours)


## Query for channels with at least 15 videos
SELECT ?channel_title ?time_to_trending_average_hours WHERE{
{SELECT ?channel_title (AVG(?time_in_seconds) as ?average_time_to_trending_seconds) WHERE {
  
  ?video a ex:Video .
  ?video ex:channel_title ?channel_title .   
  ?video ex:publish_timestamp ?publish_timestamp .
  ?video ex:trending_timestamp ?trending_timestamp
  BIND(xsd:dateTime(?trending_timestamp) - xsd:dateTime(?publish_timestamp) AS ?time2trending)    
  BIND(year(?time2trending) AS ?years)    
  BIND(month(?time2trending) AS ?months)    
  BIND(day(?time2trending) AS ?days)    
  BIND(hours(?time2trending) AS ?hours)   
  BIND(minutes(?time2trending) AS ?minutes)   
  BIND(seconds(?time2trending) AS ?seconds)   
  
  BIND( (?days*86400 + ?hours*3600 + ?minutes*60 + ?seconds) AS ?time_in_seconds)
  
}GROUP BY ?channel_title HAVING(COUNT(*)>4)}

  BIND(ceil(?average_time_to_trending_seconds/3600) AS ?time_to_trending_average_hours)
  

}ORDER BY ASC(?time_to_trending_average_hours) LIMIT 10

```

### Results - Channels

| 1    | <http://ex.org/channel/Cocina_al_Natural>                    | "1.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| ---- | ------------------------------------------------------------ | ------------------------------------------------- |
| 2    | <http://ex.org/channel/Los_Bffies>                           | "1.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 3    | <[http://ex.org/channel/TOQUE_Y_SAZ%C3%83%C2%93N](http://ex.org/channel/TOQUE_Y_SAZÃN)> | "2.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 4    | <[http://ex.org/channel/Kiwilim%C3%83%C2%B3n](http://ex.org/channel/KiwilimÃ³n)> | "2.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 5    | <http://ex.org/channel/WeroWeroTV>                           | "3.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 6    | <http://ex.org/channel/Wrestling_Universe>                   | "3.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 7    | <http://ex.org/channel/Secretos_de_la_Vida>                  | "3.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 8    | <http://ex.org/channel/Como_dice_el_dicho>                   | "3.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 9    | <http://ex.org/channel/Ivan_Donalson>                        | "3.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 10   | <http://ex.org/channel/X22Report>                            | "3.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |

### Results -  Categories

|      | category                                       | time_to_trending_average_hours                      |
| ---- | ---------------------------------------------- | --------------------------------------------------- |
| 1    | <http://ex.org/category/Shows>                 | "38.0"^^<http://www.w3.org/2001/XMLSchema#decimal>  |
| 2    | <http://ex.org/category/No_categoria>          | "39.0"^^<http://www.w3.org/2001/XMLSchema#decimal>  |
| 3    | <http://ex.org/category/Movies>                | "47.0"^^<http://www.w3.org/2001/XMLSchema#decimal>  |
| 4    | <http://ex.org/category/News_&_Politics>       | "73.0"^^<http://www.w3.org/2001/XMLSchema#decimal>  |
| 5    | <http://ex.org/category/Howto_&_Style>         | "90.0"^^<http://www.w3.org/2001/XMLSchema#decimal>  |
| 6    | <http://ex.org/category/Entertainment>         | "101.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 7    | <http://ex.org/category/Gaming>                | "119.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 8    | <http://ex.org/category/Nonprofits_&_Activism> | "120.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 9    | <http://ex.org/category/Pets_&_Animals>        | "121.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 10   | <http://ex.org/category/Sports>                | "139.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 11   | <http://ex.org/category/Autos_&_Vehicles>      | "156.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 12   | <http://ex.org/category/People_&_Blogs>        | "160.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 13   | <http://ex.org/category/Science_&_Technology>  | "169.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 14   | <http://ex.org/category/Comedy>                | "199.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 15   | <http://ex.org/category/Travel_&_Events>       | "251.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 16   | <http://ex.org/category/Film_&_Animation>      | "293.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 17   | <http://ex.org/category/Music>                 | "390.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 18   | <http://ex.org/category/Education>             | "431.0"^^<http://www.w3.org/2001/XMLSchema#decimal> |

## 5. Find the best performing (likes+comments/num_views) categories for a given tag. (top 10)

```SPARQL
SELECT (MAX(?performance) as ?m_p) WHERE {
  	?tag a tg:Funny .
  	?video a ex:Video .
    ?video ex:hasTag ?tag .
    ?video ex:category ?cat .
    ?video ex:views ?views .
    ?video ex:likes ?likes .
    ?video ex:dislikes ?dislikes .
    ?video ex:comment_count ?comments .

  BIND(((?likes + ?comments)/?views) as ?performance) .
}GROUP BY ?tag ?cat 
ORDER BY DESC(?m_p)
LIMIT 10
```



### Results

|      | cat                                           | performance                                                  |
| ---- | --------------------------------------------- | ------------------------------------------------------------ |
| 1    | <http://ex.org/category/Shows>                | "0.039612354693054087808627"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 2    | <http://ex.org/category/Movies>               | "0.043338299457273597956795"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 3    | <http://ex.org/category/No_categoria>         | "0.111380816977599001317706"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 4    | <http://ex.org/category/News_&_Politics>      | "0.122075526700499472784748"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 5    | <http://ex.org/category/Science_&_Technology> | "0.12962962962962962962963"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 6    | <http://ex.org/category/Sports>               | "0.131175432700386489665602"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 7    | <http://ex.org/category/Education>            | "0.155303641713952246737605"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 8    | <http://ex.org/category/Gaming>               | "0.186055620838229533881708"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 9    | <http://ex.org/category/Travel_&_Events>      | "0.198130841121495327102804"^^<http://www.w3.org/2001/XMLSchema#decimal> |
| 10   | <http://ex.org/category/Pets_&_Animals>       | "0.198834825763297011543856"^^<http://www.w3.org/2001/XMLSchema#decimal> |
