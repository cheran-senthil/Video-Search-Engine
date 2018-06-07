import glob
import json
import os

import py2neo

import common

# Gets all json files in test
os.chdir("./test")
json_file_names = glob.glob("*.json")

# Logs in to neo4j
Graph = common.authenticateNeo4j('localhost', 'neo4j', 'india1')

# Deletes already existing nodes and relationships
Graph.delete_all()

nodes = []

# Creates all nodes
for json_file_name in json_file_names:
    # Loads the json file
    json_file = open(json_file_name)
    data = json.load(json_file)
    json_file.close()

    # Creates a node
    node = py2neo.Node("Video")
    node["Id"] = data['videoInfo']['id']
    node["thumbnail"] = data['videoInfo']['snippet']['thumbnails']['default']['url']
    node["channelTitle"] = data['videoInfo']['snippet']['channelTitle']
    node["description"] = data['videoInfo']['snippet']['description']
    node["title"] = data["videoInfo"]["snippet"]["title"]
    if ('tags' in data['videoInfo']['snippet'].keys()):
        tags = data['videoInfo']['snippet']['tags']
    else:
        tags = 0
    node["tags"] = tags
    nodes.append(node)
    Graph.create(node)

# Creates all relationships
for node1 in nodes:
    print 1
    node1_Id = node1["Id"]
    node1_thumbnail = node1["thumbnail"]
    node1_channelTitle = node1["channelTitle"]
    node1_description = node1["description"].split()
    node1_title = node1["title"]
    node1_tags = node1["tags"]
    for node2 in nodes:
        if (node1 == node2):
            continue
        node2_Id = node2["Id"]
        node2_thumbnail = node2["thumbnail"]
        node2_channelTitle = node2["channelTitle"]
        node2_description = node2["description"].split()
        node2_title = node2["title"]
        node2_tags = node2["tags"]

        # Finds if node1 and node2 are from same channel
        same_channel = 0
        if (node1["channelTitle"] == node2["channelTitle"]):
            same_channel = 1

        # Finds the number of common title words between node1 and node2
        common_title_words = set(node1_title).intersection(set(node2_title))
        common_title = len(common_title_words)

        # Finds the number of common description words between node1 and node2
        common_description_words = set(
            node1_description).intersection(set(node2_description))
        common_description = len(common_description_words)

        # Finds the number of common tags between node1 and node2
        common_tags = []
        if (node1["tags"]) and (node2["tags"]):
            common_tags = set(node1_tags).intersection(set(node2_tags))
            common_tags_weight = len(common_tags)
        else:
            common_tags = 0

        # Creates relationships according to the data above
        if same_channel:
            relationship = py2neo.Relationship(node1, "Same_Channel", node2)
            Graph.create(relationship)
        if common_title:
            relationship = py2neo.Relationship(
                node1, "common_title", node2, weight=common_title)
            Graph.create(relationship)
        if common_description:
            relationship = py2neo.Relationship(
                node1, "common_description", node2, weight=common_description)
            Graph.create(relationship)
        if common_tags:
            relationship = py2neo.Relationship(
                node1, "common_tags", node2, weight=common_tags_weight)
            Graph.create(relationship)
