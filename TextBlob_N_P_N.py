from textblob import TextBlob

# Define a function to categorize sentiment
def categorize_sentiment(text):
    # Compute polarity using TextBlob
    if pd.isnull(text):  # Handle missing text gracefully
        return "Neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Combine Article Name and Description for sentiment analysis
df['Combined_Text'] = df['Article Name'].fillna('') + " " + df['Description'].fillna('')

# Apply the sentiment categorization
df['Sentiment'] = df['Combined_Text'].apply(categorize_sentiment)

# Summarize the sentiment distribution
sentiment_summary = df['Sentiment'].value_counts()

# Display the updated DataFrame with sentiment column and the summary
import ace_tools as tools; tools.display_dataframe_to_user(name="JD Vance Article Sentiment Analysis", dataframe=df)

sentiment_summary

