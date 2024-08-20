import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from math import log

urls = [
    "https://www.recipetineats.com/one-pot-moussaka-beef-rice-pilaf/",
    "https://www.recipetineats.com/smoky-roasted-tomato-soup/",
    "https://www.recipetineats.com/one-pot-creamy-tomato-beef-pasta/",
    "https://www.recipetineats.com/spanish-paella/",
    "https://www.recipetineats.com/lentil-soup/",
    "https://www.recipetineats.com/juicy-slow-cooker-turkey-breast/",
    "https://www.recipetineats.com/spaghetti-bolognese/",
    "https://www.recipetineats.com/mexican-ground-beef-casserole-with-rice/",
    "https://www.recipetineats.com/mexican-shredded-beef-and-tacos/",
    "https://www.recipetineats.com/quesadilla/",
    "https://www.recipetineats.com/slow-roasted-rosemary-garlic-lamb-shoulder/"
]


terms = ["onion", "tbsp", "olive", "oil"]



def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^\w\s]', ' ', text)
    return text


# שלב 1: בניית טבלת תדירות (Frequency Table)
frequency_table = pd.DataFrame(0, index=[f"URL{i + 1}" for i in range(len(urls))], columns=terms)

# שלב 2: בניית טבלת מונחים (Terms Table)
terms_table = pd.DataFrame(0, index=[f"URL{i + 1}" for i in range(len(urls))], columns=["Term Count", "Total Words"])

# עיבוד הקישורים ובניית הטבלאות
for i, url in enumerate(urls):
    # הורדת התוכן של הדף
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # חילוץ כל הטקסט מהדף
    text = soup.get_text()

    # ניקוי הטקסט
    words = clean_text(text).split()

    # ספירת כמות המילים הכוללת בדף
    total_words = len(words)

    # ספירת כמות המונחים (מילים ייחודיות) בדף
    term_count = len(set(words))

    # עדכון טבלת המונחים
    terms_table.at[f"URL{i + 1}", "Term Count"] = term_count
    terms_table.at[f"URL{i + 1}", "Total Words"] = total_words

    # עדכון טבלת התדירות
    for term in terms:
        frequency_table.at[f"URL{i + 1}", term] = words.count(term)

# שלב 3: בניית טבלת TF (Term Frequency)
tf_table = frequency_table.copy()

# חישוב ה-TF עבור כל מונח וכל דף
for url in tf_table.index:
    for term in tf_table.columns:
        tf_table.at[url, term] = tf_table.at[url, term] / terms_table.at[url, "Term Count"]

# שלב 4: בניית טבלת IDF (Inverse Document Frequency)
idf_table = pd.DataFrame(0, index=["IDF"], columns=terms)

# חישוב ה-IDF עבור כל מונח
for term in idf_table.columns:
    df = sum(frequency_table[term] > 0)  # כמות הדפים שבהם המונח מופיע
    idf_table.at["IDF", term] = log(len(urls) / (df))  # +1 למניעת חלוקה באפס

# שלב 5: בניית טבלת TF-IDF
tfidf_table = tf_table.copy()

# חישוב ה-TF-IDF עבור כל מונח וכל דף
for url in tfidf_table.index:
    for term in tfidf_table.columns:
        tfidf_table.at[url, term] = tf_table.at[url, term] * idf_table.at["IDF", term]

# שמירת הטבלאות לקובצי Excel
frequency_table.to_excel('frequency_table.xlsx', index=True)
terms_table.to_excel('terms_table.xlsx', index=True)
tf_table.to_excel('tf_table.xlsx', index=True)
idf_table.to_excel('idf_table.xlsx', index=True)
tfidf_table.to_excel('tfidf_table.xlsx', index=True)

print("הטבלאות נשמרו בקבצי Excel.")
