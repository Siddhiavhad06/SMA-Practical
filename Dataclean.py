import pandas as pd
import re

# Define a function for cleaning the tweet text
def clean_tweet(tweet):
    # Remove URLs
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
    
    # Remove user mentions (e.g., @username)
    tweet = re.sub(r'@\w+', '', tweet)
    
    # Remove hashtags (optional — keep if needed)
    tweet = re.sub(r'#\w+', '', tweet)
    
    # Remove special characters and digits
    tweet = re.sub(r'[^A-Za-z\s]', '', tweet)
    
    # Convert text to lowercase
    tweet = tweet.lower()
    
    # Split tweet into words (tokenization without NLTK)
    words = tweet.split()
    
    # Remove stopwords manually (optional — you can customize the stopwords list)
    stopwords = set([
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 
        'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 
        'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 
        'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 
        'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
    ])
    
    filtered_words = [word for word in words if word not in stopwords]
    
    # Remove emojis (convert to ASCII and ignore non-ASCII chars)
    tweet = ' '.join(filtered_words)
    tweet = tweet.encode('ascii', 'ignore').decode('ascii')
    
    return tweet

# Step 2: Load the dataset
dataset_path = r"C:\Users\mehul\OneDrive\Desktop\sma\datacleaning\twitter_dataset.csv"  # Use raw string for Windows paths

# Step 3: Read the dataset (CSV format)
df = pd.read_csv(dataset_path)

# Step 4: Check the column names
print("Columns in the dataset:", df.columns)

# Step 5: Apply the cleaning function to the correct column
# Assuming the column name is 'Text'
df['cleaned_text'] = df['Text'].apply(clean_tweet)

# Step 6: Check the cleaned data
print(df[['Text', 'cleaned_text']].head())

# Step 7: Optionally, save the cleaned data to a new CSV file
cleaned_path = "cleaned_twitter_dataset.csv"
df.to_csv(cleaned_path, index=False)

print("Cleaned dataset saved to:", cleaned_path)