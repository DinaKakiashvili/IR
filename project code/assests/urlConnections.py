import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

# רשימת הקישורים שלך
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

# יצירת מיפוי בין URL למספר מזהה
url_to_index = {url: str(i + 1) for i, url in enumerate(urls)}

# יצירת גרף ריק
G = nx.DiGraph()

# הוספת הצמתים לגרף
for url, index in url_to_index.items():
    G.add_node(index)

# מעבר על כל URL ובדיקת קישורים יוצאים
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # חיפוש כל הקישורים בתוך הדף
    for link in soup.find_all('a', href=True):
        href = link['href']
        # בדיקה אם הקישור מוביל לאחד ה-URLs ברשימה
        for target_url in urls:
            if href.startswith(target_url) and url != target_url:  # להתעלם מקשרים לצומת עצמו
                G.add_edge(url_to_index[url], url_to_index[target_url])

# הדפסת הקשרים עם מספרים
for edge in G.edges():
    print(f"{edge[0]} -> {edge[1]}")

# ציור הגרף עם התאמות לעיצוב
plt.figure(figsize=(12, 10))  # הרחבת המרווחים בין הצמתים
pos = nx.spring_layout(G, k=0.5)  # שימוש בפרמטר 'k' לשליטה במרווחים
nx.draw(G, pos, with_labels=True, node_color='skyblue', font_weight='bold', font_size=10, node_size=2000,
        edge_color='gray')  # הקטנת גודל העיגולים
plt.title('URL Linking Graph with Node Numbers')
plt.show()

# הדפסת המיפוי בין מספרים ל-URLs
print("\nMapping of Numbers to URLs:")
for url, index in url_to_index.items():
    print(f"{index}: {url}")
