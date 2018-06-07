import sqlite3

import py2neo
import pymongo


# def createSQLdb():
#    try:
#        conn = sqlite3.connect('videodb.db')
#        c = conn.cursor()
#        c.execute('''CREATE TABLE userclick (user, youtubeid, query)''')
#    except:
#        print


def updateSQLdb(username, youtubeid, query):
    try:
        conn = sqlite3.connect('videodb.db')
        conn.execute('INSERT INTO userclick VALUES (?,?,?);',
                     (username, youtubeid, query))
    except:
        print



def writeToFile(File_name, content):
    with open(File_name, 'w') as File:
        content = content.encode("utf-8")
        File.write(content)


def createButton(Video_Id, thumbnail_url, title):
    thumbnail_url = thumbnail_url.decode("utf-8")
    title = title.decode("utf-8")
    button = "<button type='submit' class='searchResult' name='Video' value='%s'><img src='%s'><br>%s</button>\n"
    button = button % (Video_Id, thumbnail_url, title)
    return button


def authenticateNeo4j(host, user, password):
    try:
        Graph = py2neo.Graph(host=host, user=user, password=password)
    except:
        writeToFile("temp.html", "Unable to access neo4j")
        exit()
    return Graph


def getCollection(host, db_name, collection_name):
    client = pymongo.MongoClient(host, 27017)
    db = client[db_name]
    collection = db[collection_name]
    return collection


def getRecommendations(Graph, video_id):
    buttons = []
    reco_list = []
    sorted_list = []

    node = Graph.find_one("Video", "Id", video_id)

    for rel in Graph.match(start_node=node):
        video_id = ' ' + rel.end_node()["Id"]
        thumbnail_url = rel.end_node()["thumbnail"]
        title = rel.end_node()["title"].encode("utf-8")
        button = createButton(video_id, thumbnail_url, title)
        weight = 8
        if rel["weight"]:
            reco_list.append([video_id, rel["weight"], button])

    sorted_list = sorted(reco_list, key=lambda x: x[0], reverse=True)

    tmp = ""
    count = 0
    for i in sorted_list:
        if (tmp == i[0]):
            sorted_list[count - 1][1] += sorted_list[count][1]
            tmp = i[0]
            sorted_list[count][1] = 0
        else:
            tmp = i[0]
        count += 1
    count = 0
    for i in sorted_list:
        if (i[1] == 0):
            del sorted_list[count]
        count += 1

    sorted2 = sorted(sorted_list, key=lambda x: x[1], reverse=True)

    for i in sorted2:
        buttons.append(i[2])

    return "".join(buttons)
