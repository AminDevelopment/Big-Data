from dotenv import load_dotenv, find_dotenv
import os
import sys
from pymongo import MongoClient
import AddDataNodes

def find_disease(nodes, disease):
    diseased = nodes.find_one({"id":disease})
    print(diseased)

def main():
    # Inputs from terminal
    disease_id = sys.argv[1]

    # Basic connection to MongoDB
    load_dotenv(find_dotenv())
    password = os.environ.get("MONGODB_PWD")
    connection_string = f"mongodb+srv://nabeelamin4:{password}@cluster0.m1yiwlb.mongodb.net/test"
    client = MongoClient(connection_string)

    # Find out if user wants to input data to database
    run_module = input("Do you want to run AddDataNodes to add Nodes.tsv and Edge.tsv to MongoDB?: ")
    if run_module.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
        print("Ok running AddDataNodes, this will take some time.")
        AddDataNodes.main()
    
    # Find diesease with given query from terminal
    bigData_db = client["BigData"]
    nodes_collections = bigData_db.nodes
    find_disease(nodes_collections, disease_id)


if __name__ == "__main__":
    main()

