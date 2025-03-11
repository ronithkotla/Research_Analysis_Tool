import requests
from serpapi.google_search import GoogleSearch
import re
API_KEY="AIzaSyAY_vxL36U2L0qKSsvlMTEykeAEYqpQXDY"
SEARCH_ENGINE_ID="2475e772c459942ea"


def get_search_links(topic):
    
    url="https://www.googleapis.com/customsearch/v1"


    params={
        'q': topic,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'gl': "in",
        'hl': "en",
        'num': 4,
    }

    response=requests.get(url,params=params)
    results=response.json()

    # Normal Search Results
    if 'items' in results:
        links=[]
        title=[]
        snippet=[]
        for i in results['items']:
            links.append(i["link"])
            title.append(i['title'])
            snippet.append(i["snippet"])
        return title,links,snippet


def get_images(topic):
    url="https://www.googleapis.com/customsearch/v1"
    params={
    'q': topic,
    'key': API_KEY,
    'cx': SEARCH_ENGINE_ID,
    'gl': "in",
    'hl': "en",
    'num': 4,
    'searchType': "image",   
    }

    response=requests.get(url,params=params)
    results=response.json()
    if 'items' in results:
        img_links=[]
        for img in results['items']:
           img_links.append(img["link"])
        return img_links


def get_videos(topic):
    params = {
    "engine": "google",
    "q": topic,
    "api_key": "f332815c242a97bff44646d6d86bc03af10eb74c616ec905553fb064a6aed317",
    "gl": "in",
    "cr": "countryIN",
    "num":4,
    "tbm":"vid"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    pattern = r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+'
        # Find all matches in the text
    matches = list(set(re.findall(pattern, str(results))))
    return matches

def get_pdfs(topic):
    url="https://www.googleapis.com/customsearch/v1"

    params={
        'q': topic,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'gl': "in",
        'hl': "en",
        'num': 4,
        "fileType":"pdf",

    }

    response=requests.get(url,params=params)
    results=response.json()
    if 'items' in results:
        pdf_links=[]
        for pdf in results['items']:
           pdf_links.append(pdf["link"])
        return pdf_links

    

def get_news(topic):
    params = {
    "engine": "google",
    "q": topic,
    "api_key": "f332815c242a97bff44646d6d86bc03af10eb74c616ec905553fb064a6aed317",
    "gl": "in",
    "num":4,
    "tbm":"nws"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    news_titles=[]
    news_links=[]
    news_snippets=[]
    try:
        for news in results["news_results"]:
            news_titles.append(news["title"])
            news_links.append(news["link"])
            news_snippets.append(news["snippet"])
    except:
        return news_titles,news_links,news_snippets

    return news_titles,news_links,news_snippets