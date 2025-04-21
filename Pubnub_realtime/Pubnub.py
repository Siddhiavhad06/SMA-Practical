from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import random
import time
import csv
import os
from datetime import datetime

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-03183bd3-423e-435f-8236-8afe94fb2c09'
pnconfig.subscribe_key = 'sub-c-6ebb8931-e9fa-4366-bac5-870e75f8558b'
pnconfig.uuid = 'social_media_stream'

pubnub = PubNub(pnconfig)

# Simulated users, topics, etc.
users = ['@elonmusk', '@nasa', '@techguru', '@gptbot']
topics = ['AI', 'SpaceX', 'Mars', 'Tech', 'ChatGPT', 'Bitcoin']
locations = ['California', 'New York', 'Texas', 'India', 'Germany', 'Tokyo']
sentiments = ['positive', 'neutral', 'negative']

# ✅ Save CSV to Desktop
csv_file = 'C:\\Users\\Hp\\OneDrive\\Desktop\\ADS Project\\social_stream.csv'
file_exists = os.path.isfile(csv_file)

# Write CSV headers if file doesn't exist
if not file_exists:
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Timestamp', 'User', 'Topic', 'Message',
            'Likes', 'Retweets', 'Sentiment', 'Location'
        ])

# Start publishing + writing loop
while True:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = {
        'timestamp': timestamp,
        'user': random.choice(users),
        'topic': random.choice(topics),
        'message': f"Trending: {random.choice(topics)} is blowing up!",
        'likes': random.randint(10, 1000),
        'retweets': random.randint(5, 500),
        'sentiment': random.choice(sentiments),
        'location': random.choice(locations)
    }

    # Publish to PubNub channel
    pubnub.publish().channel('social_stream').message(message).sync()
    print(f"Published: {message}")

    # Append to CSV
    try:
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                message['timestamp'], message['user'], message['topic'],
                message['message'], message['likes'], message['retweets'],
                message['sentiment'], message['location']
            ])
    except PermissionError:
        print(" CSV is open elsewhere. Please close it and rerun.")
    
    time.sleep(2)  # Publish every 2 seconds