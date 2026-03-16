import requests
import pandas as pd
import time

def get_nyt_news(year, month, api_key):
    # L'API Archive du NYT renvoie tout un mois de données
    url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={api_key}"
    
    print(f"Extraction des archives pour {month}/{year}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data['response']['docs']
        return articles
    else:
        print(f"Erreur : {response.status_code}")
        return []

# --- CONFIGURATION ---
MY_API_KEY = "VOTRE_CLE_API_ICI"
TARGET_DATE = "2000-01-01"

# 1. Récupérer les articles du mois concerné
all_articles = get_nyt_news(2000, 1, MY_API_KEY)

# 2. Filtrer pour ne garder que le 1er janvier 2000
daily_news = []
for art in all_articles:
    # La date est au format '2000-01-01T00:00:00+0000'
    if art['pub_date'].startswith(TARGET_DATE):
        daily_news.append({
            'date': art['pub_date'],
            'headline': art['headline']['main'],
            'section': art.get('section_name', 'N/A'),
            'abstract': art.get('abstract', 'N/A')
        })

# 3. Affichage des résultats
df = pd.DataFrame(daily_news)

if not df.empty:
    print(f"\n{len(df)} articles trouvés pour le {TARGET_DATE} :")
    # On affiche surtout les sections Finance/Business pour votre analyse
    business_news = df[df['section'].str.contains("Business", na=False)]
    print(business_news[['headline', 'section']].head(10))
else:
    print("Aucun article trouvé pour cette date spécifique.")