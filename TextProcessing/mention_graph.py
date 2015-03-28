""" Extract user mentions for all users to create information flow graph
"""
import json
import os
import time
import datetime
import logging
import csv
import pickle

todayDate = []
today = datetime.date.today()
todayDate.append(today)

def extractTweets():
  logging.basicConfig(filename='./extractUserMentions_'+ str(todayDate[0]) + '.log',level=logging.DEBUG)
  company_list = ['amazon','apple','cisco','dropbox','ebay','facebook','foursquare',\
                  'google','ibm','intel','microsoft', 'qualcomm','twitter']
  count = 0
  tweet_count = 0
  fieldnames=["userid", "user_company", "mentions", "mention_company"]
  user_dict = pickle.load( open( "user_dict.p", "rb" ) )
  for company in company_list:
        output_file = open('./'+ company + '_user_mentions.csv', 'w')
        writer =  csv.DictWriter(output_file,fieldnames=fieldnames)
        count = 0
  	for file in os.listdir('../'+company):
                if file.endswith(".txt"):
                  continue
                try:
  	   	  json_data = open('../'+company+'/'+file).read()
  		  data = json.loads(json_data)
                except:
                  logging.warning('Parsing of file %s failed', file)
                else:
  	  	  if len(data):
                    count += 1
  		    for item in data:
                        if item['entities']['user_mentions']:
                            for mentions in item['entities']['user_mentions']:
                                try:
                                  mention_company = user_dict[int(mentions['id'])]
                                except KeyError:
                                  mention_company = "NULL"
                                if item['user']['id'] != int(mentions['id']):
                                  writer.writerow({'userid' : item['user']['id'], 'user_company' : company, 'mentions' : mentions['id'], 'mention_company' : mention_company })
                                  tweet_count += 1
	            logging.info('Wrote co-ordinates of %d from company %s', item['user']['id'], company)
        print "Done extracting data for ",company
        logging.debug('Wrote a total of %d tweets for company %s', count, company)
  print "Processed a total of", tweet_count, "tweets"

if __name__ == '__main__':
	extractTweets()
