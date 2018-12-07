import urllib.request
import json

# 324991-stuy-YAU093CG

def get_key(key_type):
    '''Gets the api key from keys.JSON base on the key_type'''
    with open('keys.JSON', 'r') as f:
        keys = json.load(f)
        print(keys)
    return keys.get(key_type)

def google_books_data(query):
    '''Returns the search results from google books api using the given
    query. Results are returned in the form of a dictionary'''
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
    '''Returns the recommended books from tastedive api using the given
    book title. Results are returned in the form of a list containing dictionaries'''
    url_stub = "https://tastedive.com/api/similar?"
    api_key = get_key('tastedive_book')
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
        try:
            for book in data["Similar"]["Results"][0:6]:
                if (book.get("Type")=="book"):
                    book_title = remove_nonascii(book.get("Name").replace(" ", "+"))
                    dict = google_books_data(book_title)
                    if (dict.get("totalItems")!=0):
                        list.append(dict)
        except KeyError as e:
            print("tastedive not working")
    except urllib.error.HTTPError as err:
        print("Invalid url request, something went wrong" )
        list = []
    return list[0:8]

def remove_nonascii(text):
    '''Removes the non-ascii characters from the text and returns it.'''
    text = ''.join(i for i in text if ord(i)<128)
    #text = ''.join(i for i in text if i=="%")
    return text

def name_from_id(id):
    '''Retrieves book name based on id'''
    try:
        data = google_books_data(id)
        return data.get("items")[0]["volumeInfo"]["title"]
    except:
        return "Paradise Lost"
