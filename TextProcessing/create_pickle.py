import json
import os
import pickle
from collections import defaultdict

def extractTweets():
  company_list = ['amazon','apple','cisco','dropbox','ebay','facebook','foursquare',\
                  'google','ibm','intel','microsoft', 'qualcomm','twitter']

  user_dict = {} 
  for company in company_list:
        print company
        for file in os.listdir('../'+company):
                if not file.endswith(".json"):
                  continue
                user_id = int(file.split(".")[0])
                print user_id
                try:
                   user_dict[user_id]
                except KeyError:
                   user_dict[user_id] = company


  print "dictionary created, dumping..."
  print type(user_dict.keys()[1])
  print user_dict.items()
  pickle.dump(user_dict, open( "user_dict.p", "wb" ))


if __name__ == "__main__":
    extractTweets()
