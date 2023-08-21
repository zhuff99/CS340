from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse

"""
Project 1 CS340 
Zachary Huff
August 3, 2023
CRUD Python file for MongoDB
"""

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
      
    def __init__(self, password = "pass", username = 'aacuser'):      #Changed in module 5 to make __init__ have 2 additional inputs password/username
        
        #urllib to parse username and pass
        #https://pymongo.readthedocs.io/en/stable/examples/authentication.html
        userName = urllib.parse.quote_plus(username)
        password = urllib.parse.quote_plus(password)
        
        self.client = MongoClient('mongodb://%s:%s@localhost:27017/?authSource=aac' % (userName, password)) #Mongo login with localhost, default port, and user/pass to login
        self.database = self.client['aac']
       

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            insert = self.database.animals.insert_one(data)  # data should be dictionary
            if insert != 0:
                return True
            else:
                return False            
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Create method to implement the R in CRUD.

    def read(self,row=None):

        # Check to make sure row fields are not empty.
        if row:    
            data = self.database.animals.find(row,{"_id":False})
        else:
        #return empty list if rows are empty
            data = self.database.animals.find( {} , {"_id":False})
        return data
    
    # Create method for implementing the U in CRUD.

    def update(self, data, dataToUpdate):
        if not data:
            print("No data found")
        elif not dataToUpdate:
            print("No data to update.")
        else:
            updateValid = self.database.animals.update_many(data, {"$set": dataToUpdate}) #replace old data with updated data
            self.records_updated = updateValid.modified_count
            self.records_matched = updateValid.matched_count 
             
            return True if updateValid.modified_count > 0 else False        ##return true if update count > 0
            
    # Create method for implementing the D in CRUD
    
    def delete(self, data):
        if data is not None:
            delete = self.database.animals.delete_many(data)  # data should be dictionary
            if delete != 0:
                return self.read(data)
            else:
                raise Exception("Nothing to delete, because data parameter is empty")
            
    
    #This method was created for module 5 assignment because my read method has row=None as default
    #which doesnt allow for user input to search for specified information
    #it takes in record information and will parse by the given information
    
    def recordSearch(self, find):
        if find:
            data = self.database.animals.find(find, {'_id' : 0})
                                 
        else:
            data = self.database.animals.find({}, {'_id' : 0})
                                  
        return data