""" Extract friends of each user and match with other companies.
    Write results to a single file for each company.
"""

import json
import os
import csv
import pickle
import glob

def extract_friends():
  company_list = ['amazon','apple','cisco','dropbox','ebay','facebook','foursquare',\
                  'google','ibm','intel','microsoft', 'qualcomm','twitter']

  fieldnames=["userid", "user_company", "friend_id", "friend_company"]
  user_dict = pickle.load( open( "user_dict.p", "rb" ) )
  for company in company_list:
        output_file = open('./'+ company + '/' + 'all_friends.csv', 'w')
        writer =  csv.DictWriter(output_file,fieldnames=fieldnames)
        for file in glob.glob('./'+company+'/*friend*'):
          file = file.split("/")[2]
          print file
          if not file.endswith(".json"):
            continue
          try:
            json_data = open('./'+company+'/'+file).read()
            data = json.loads(json_data)
          except:
            print "Warning. Wrong file..."
          else:
            if len(data):
              user_id = int( (file.split(".")[0]).split("_")[0] )
              for item in data:
                try:
                  friend_company = user_dict[int(item)]
                except KeyError:
                  friend_company = "NULL"
                #if friends_company != "NULL":
                  #writer.writerow({'userid' : user_id, 'user_company' : company, 'friend_id' : item, 'friend_company' : friend_company })
                  
if __name__ == "__main__":
  extract_friends()
