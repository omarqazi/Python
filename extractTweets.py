""" Extract tweets from all files and write a csv file with fields :
    userid,tweet,post-date
"""
import json
import os
import time
import datetime
import logging
import csv

todayDate = []
today = datetime.date.today()
todayDate.append(today)

def extractTweets():
  logging.basicConfig(filename='./extractTweets_'+ str(todayDate[0]) + '.log',level=logging.DEBUG)
  company_list = ['amazon','apple','cisco','dropbox','ebay','facebook','foursquare',\
                  'google','ibm','intel','microsoft', 'qualcomm','twitter']
  count = 0
  tweet_count = 0
  fieldnames=["text","user","date"]
  for company in company_list:
        output_file = open('./' + company +'/' + company + '.csv', 'w')
        writer =  csv.DictWriter(output_file,fieldnames=fieldnames) 
        count = 0
  	for file in os.listdir(company):
                if file.endswith(".txt"):
                  continue
                try:
  	   	  json_data = open('./'+company+'/'+file).read()
  		  data = json.loads(json_data)
                except:
                  logging.warning('Parsing of file %s failed', file)
                else:  
  	  	  if len(data):
                    count += 1
  		    for item in data:
  		  	    formatted_date = time.strftime('%Y-%m-%d', time.strptime(item['created_at'], \
  				                               '%a %b %d %H:%M:%S +0000 %Y'))
                            if item['lang'] == 'en':
  			      tweet = item['text'].strip()
  			      tweet = tweet.replace('\\n',"")
  			      tweet = tweet.replace('\\t',"")                            
  			      #print str(item['user']['id']) + ",\"" + tweet + "\"," + formatted_date
                              writer.writerow({'user':item['user']['id'],'text':tweet.encode('utf-8').strip(),'date':formatted_date})
                              #output_file.write("%s,%s,%s" % (item['user']['id'],"\"" + tweet.encode('utf-8').strip() + "\"",formatted_date+'\n'))
                              tweet_count += 1
		    logging.info('Wrote tweets of %d from company %s', item['user']['id'], company)
        print "Done extracting data for ",company
        logging.debug('Wrote a total of %d tweets for company %s', count, company)
  print "Processed a total of", tweet_count, "tweets"

if __name__ == '__main__':
	extractTweets()
