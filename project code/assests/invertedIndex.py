import requests
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import re
import pandas as pd

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

stop_words = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now','pm'
])

def clean_text(text):

    text = text.lower()

    text = re.sub(r'\W+|\d+', ' ', text)
    return text


inverted_index = defaultdict(list)


all_common_words = []


for i, url in enumerate(urls, start=1):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    text = soup.get_text()


    words = clean_text(text).split()


    words = [word for word in words if word not in stop_words]


    word_counter = Counter(words)


    common_words = [word for word, count in word_counter.most_common(15)]


    all_common_words.extend(common_words)


final_common_words = [word for word, count in Counter(all_common_words).most_common(15)]


for i, url in enumerate(urls, start=1):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')


    text = soup.get_text()


    words = clean_text(text).split()


    words = [word for word in words if word not in stop_words]


    for word in final_common_words:
        if word in words:
            inverted_index[word].append(i)


df = pd.DataFrame(list(inverted_index.items()), columns=['Word', 'Page Indices'])


df.to_excel('inverted_index_with_indices.xlsx', index=False)

print("התוצאות נשמרו בקובץ 'inverted_index_with_indices.xlsx'")
