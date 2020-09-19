import praw
import schedule
import json
import time
import csv

#### Initializing praw
reddit = praw.Reddit('bot1')


#### Read the currently tracked IDs
def gather_data():
  tracking_ids = []

  with open('tracking_ids.csv') as f:
    csv_reader = csv.DictReader(f)
    track_flag = False
    for row in csv_reader:
      tracking_ids.append(row)
      track_flag = True


  #### Check if there are tracking IDs, if not, gather new ones and start collecting data
  with open('post-data.csv', 'a', newline='') as f:
    csv_writer = csv.writer(f)

    if not track_flag: # If empty tracking file, populate with 'hot' posts
      print('Tracking file empty, populating...')
      

      for submission in reddit.front.rising(limit=50):
        tracking_ids.append({'id': submission.id, 'created': submission.created_utc})
        csv_writer.writerow([submission.id, time.time(), submission.num_comments, submission.score])
        
      
      with open('tracking_ids.csv', 'w', newline='') as track_file:
        trackid_writer = csv.writer(track_file)
        trackid_writer.writerow(['id', 'created'])

        for item in tracking_ids:
          print(item['id'])
          trackid_writer.writerow([item['id'], item['created']])
    
    else:
    # Gather tracked post data
      for tracking_objects in tracking_ids:
        submission = reddit.submission(id=tracking_objects['id'])
        csv_writer.writerow([submission.id, time.time(), submission.num_comments, submission.score])


#### Clear out the data
def reset_data():
  f = open('tracking_ids.csv', 'w')
  f.truncate()
  f.close()


schedule.every().hour.at(':30').do(gather_data)

schedule.every().tuesday.at('16:15').do(reset_data)

while True:
    schedule.run_pending()
    time.sleep(1)