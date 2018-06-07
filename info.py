import argparse
import json
from string import Template

import common


def getInfo(collection, video_id):
    data = collection.find({'videoInfo.id': video_id})
    title = data[0]['videoInfo']['snippet']['title']
    views = data[0]['videoInfo']['statistics']['viewCount']
    likes = data[0]['videoInfo']['statistics']['likeCount']
    dislikes = data[0]['videoInfo']['statistics']['dislikeCount']
    channel = data[0]['videoInfo']['snippet']['channelTitle']
    published = data[0]['videoInfo']['snippet']['publishedAt']
    favorites = data[0]['videoInfo']['statistics']['favoriteCount']
    thumbnail = data[0]['videoInfo']['snippet']['thumbnails']['default']['url']
    try:
        tags = ", ".join(data[0]['videoInfo']['snippet']['tags'])
    except KeyError:
        tags = ""
    description = data[0]['videoInfo']['snippet']['description'].replace(
        "\n", "<br>")
    return title, views, likes, dislikes, channel, tags, description, published, favorites, thumbnail


# Gets command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("video_id", type=str)
args = parser.parse_args()
video_id = args.video_id[1:]

# Connects to Neo4j server
Graph = common.authenticateNeo4j("localhost", "neo4j", "india1")

# Connects to Mongodb server
collection = common.getCollection('localhost', "videodb", "videos")
query = ""
f = open("Info.html")
content = f.read()
f.close()
recommendation = common.getRecommendations(Graph, video_id)
title, views, likes, dislikes, channel, tags, description, published, favorites, thumbnail = getInfo(
    collection, video_id)
i = dict(id=video_id,
         title=title,
         views=views,
         likes=likes,
         dislikes=dislikes,
         channel=channel,
         tags=tags,
         description=description,
         recommendation=recommendation,
         published=published,
         favorites=favorites)
button = common.createButton(video_id, thumbnail, title)
with open('history.json') as jsondata:
    x = json.load(jsondata)
x.insert(0, button)
with open('history.json', 'w') as outfile:
    json.dump(x, outfile)
html = Template(content)
html = (html.safe_substitute(i))
common.updateSQLdb("neo4j", video_id, query)
common.writeToFile("temp.html", html)
