# Reloading the dataset since VADER wasn't used in the earlier attempt
file_path = "/mnt/data/JD Vance Article Annotations - media_stack_unique.csv"
df = pd.read_csv(file_path)

# Combine relevant columns for sentiment analysis
df['Combined_Text'] = df['Article Name'].fillna('') + " " + df['Description'].fillna('')

# Reattempt sentiment analysis with TextBlob since VADER is unavailable
from textblob import TextBlob

# Define a function for sentiment analysis using TextBlob
def textblob_sentiment_polarity(text):
    if pd.isnull(text):
        return 0.0
    return TextBlob(text).sentiment.polarity

# Add polarity score to the dataset
df['Polarity_Score'] = df['Combined_Text'].apply(textblob_sentiment_polarity)

# Display the updated dataset for user inspection
import ace_tools as tools; tools.display_dataframe_to_user(name="JD Vance Article Sentiment Polarity", dataframe=df)

df['Polarity_Score'].describe()
