import argparse
import re

import common


def findWord(w, s):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search(s)


def neo4jQueryregular(args):
    ret = ""
    j = len(args)  # Number of Search strings given
    print "hello"
    for i in range(j):
        if (i == 0):
            ret += "MATCH(n) WHERE n.title =~ '%s' OR n.description =~ '%s' OR n.tags2 =~ '%s'" % (
                args[i], args[i], args[i])
        else:
            ret += " OR n.title) =~ '%s' OR n.description) =~ '%s' OR n.tags2) =~ '%s'" % (
                args[i], args[i], args[i])
        if ((i + 1) == j):
            ret += " RETURN n"
    return ret


def neo4jQuery(args):
    ret = ""
    j = len(args)  # Number of Search strings given
    for i in range(j):
        if (i == 0):
            ret += "MATCH(n) WHERE toLOWER(n.title) CONTAINS toLOWER('%s') OR toLOWER(n.description) CONTAINS toLOWER('%s') OR toLOWER(n.tags2) CONTAINS toLOWER('%s')" % (
                args[i], args[i], args[i])
        else:
            ret += " OR toLOWER(n.title) CONTAINS toLOWER('%s') OR toLOWER(n.description) CONTAINS toLOWER('%s') OR toLOWER(n.tags2) CONTAINS toLOWER('%s')" % (
                args[i], args[i], args[i])
        if ((i + 1) == j):
            ret += " RETURN n"
    return ret


def searchAll(Graph, search_string):
    search_list = []
    sorted_list = []
    ret = []
    query = neo4jQuery(search_string)
    if search_string[0] == "advancesearch:":
        query = neo4jQueryregular(search_string[1:])
    for node in Graph.run(query):
        title_count = description_count = tags2_count = weight = 0

        Id = node["n"]["Id"]
        thumbnail_url = node["n"]["thumbnail"]
        title = (node["n"]["title"]).encode("utf-8")
        description = (node["n"]["description"]).encode("utf-8")
        tags = node["n"]["tags"]
        if tags:
            tags2 = ("".join(tags)).encode("utf-8")

        for string in search_string:
            if findWord(string, title):
                title_count += 1
            if findWord(string, description):
                description_count += 1
            if findWord(string, tags2):
                tags2_count += 1
            weight = title_count * 100 + description_count * 40 + tags2_count * 10

        search_list.append([common.createButton(
            ' ' + Id, thumbnail_url, title), weight])

    sorted_list = sorted(search_list, key=lambda x: x[1], reverse=True)

    for i in sorted_list:
        ret.append(i[0])
    if len(ret) == 0:
        return "<h3> No Results Found </h3>"
    return ret


# Gets input from command line
parser = argparse.ArgumentParser()
parser.add_argument("search_string", type=str)
args = parser.parse_args()

# Connects to Neo4j server
Graph = common.authenticateNeo4j("localhost", "neo4j", "india1")

print searchAll(Graph, args.search_string.split())
buttons = ''.join(searchAll(Graph, args.search_string.split()))
f = open("search.html")
content = f.read()
f.close()
content = content.replace('%s', buttons)
common.writeToFile("./temp.html", content)
