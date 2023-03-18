from dotenv import load_dotenv, find_dotenv
import os
import sys
from pymongo import MongoClient
import pandas as pd
import json
import csv

# Basic connection to MongoDB
load_dotenv(find_dotenv())

# Change following for individual accounts
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://nabeelamin4:{password}@cluster0.m1yiwlb.mongodb.net/test"

client = MongoClient(connection_string)
bigData_db = client["BigData"]
nodes_collections = bigData_db.nodes

# PUT IN NODE DATA
def insert_nodes(nodes, filename, header=None):
    data = pd.read_csv(filename, header=header)
    data.to_dict('records')
    nodes.insert_many(data)
    
    
# PUT IN EDGE DATA
completed_amount = 0

# Updates the data in the nodes collection 
def addinData(left, mid, right):
    global completed_amount
    # Use when inserting to check progress
    # print("Index value: " + left + ", Action value is: " + mid + ", Right value is:: " + right)
    try:
        nodes_collections.update_one({"id":left}, {"$set":{mid:right}})
    except:
        print("This did not work")

    completed_amount += 1
    # Use when inserting to check progress
    # print( str(completed_amount) + "/1,292,204 completed")
    
# Splits the data in edges.tsv
def splitValues(string):
    values = string[0].split('\t')
    addinData(values[0], values[1], values[2])


# Run insertions
def main():
    insert_nodes(nodes_collections, 'nodes.tsv')
    edges = pd.read_csv('edges.tsv')
    edges.apply(splitValues, axis=1)


if __name__ == "__main__":
    main()

