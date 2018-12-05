import urllib.request
import json

# 324991-stuy-YAU093CG
def google_books_data(query):
    url="https://www.googleapis.com/books/v1/volumes?q=" + query
    print(url)
    try:
        response = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        info = urllib.request.urlopen(response)
        info =json.load(info)
    except urllib.error.HTTPError as err:
        print("Invalid url request, something went wrong" )
        info={}
    return info

def book_rec(book_name):
    url_stub = "https://tastedive.com/api/similar?"
    api_key = "k=324991-stuy-YAU093CG"
    parameter = "&q=book:"
    search = parameter + book_name
    url = url_stub + api_key + search

    hdr = { 'User-Agent' : 'Mozilla/5.0' }

    try:
        req = urllib.request.Request(url, headers=hdr)
        url_object = urllib.request.urlopen(req)

        print("-------------------------\n")
        print(url)
        print("-------------------------\n")
        print(url_object)
        print("-------------------------\n")
        info = url_object.read()
        print("-------------------------\n")
        print(info)
        print("-------------------------\n")
        data = json.loads(info)
        list = []
        for book in data["Similar"]["Results"][0:6]:
            if (book.get("Type")=="book"):
                book_title = remove_nonascii(book.get("Name").replace(" ", "+"))
                dict = google_books_data(book_title)
                if (dict.get("totalItems")!=0):
                    list.append(dict)
    except urllib.error.HTTPError as err:
        print("Invalid url request, something went wrong" )
        list = []
    return list[0:8]

def remove_nonascii(text):
    text = ''.join(i for i in text if ord(i)<128)
    #text = ''.join(i for i in text if i=="%")
    return text
