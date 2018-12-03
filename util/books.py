import urllib.request as urlrequest
import json

# 324991-stuy-YAU093CG
def google_books_data(query):
    url="https://www.googleapis.com/books/v1/volumes?q=" + query
    print(url)
    response = urlrequest.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    info = urlrequest.urlopen(response)
    info =json.load(info)
    return info
