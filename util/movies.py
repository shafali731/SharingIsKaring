import urllib.request, json, os

#OMDb apikey=1891fe35
#tastedive 324992-SoftdevP-U4MUASLY

def get_key(key_type):
    '''Gets the api key from keys.JSON base on the key_type'''
    with open('keys.JSON', 'r') as f:
        keys = json.load(f)
        print(keys)
    return keys.get(key_type)

def remove_nonascii(text):
    '''removes non_ascii characters'''
    text = ''.join(i for i in text if ord(i)<128)
    #text = text.replace("&", "")
    return text

def movie_info(parameter, value):
    '''retrieves movie information from OMDb API based on the parameter and value'''
    try:

        url_stub = "http://www.omdbapi.com/?"
        api_key = get_key('OMDB')
        search = parameter + remove_nonascii(value)
        url = url_stub + api_key + search

        url_object = urllib.request.urlopen(url)
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
    except :
        print("Invalid url request, something went wrong" )
        data={}
    return data;

def better_movie_list(old_list):
    '''makes a more comprehensive list of movie dictionaries (initially generated from tastedive) using OMDb'''
    new_list = []
    if isinstance(old_list, list):
        for movie in old_list:
            dict = movie_info("&i=", movie.get("imdbID"))
            if (dict.get("Response")=="True"):
                dict["site_link"] = "/movie_info/" + movie.get("imdbID")
                new_list.append(dict)
    return new_list

def movie_rec(parameter, value):
    '''retrieves movie recommendations based on the parameter and value'''
    url_stub = "https://tastedive.com/api/similar?"
    api_key = get_key('tastedive_movie')
    search = parameter + value
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
            for movie in data["Similar"]["Results"]:
                if (movie.get("Type")=="movie"):
                    movie_title = remove_nonascii(movie.get("Name").replace(" ", "+"))
                    dict = movie_info("&t=", movie_title)
                    if (dict.get("Response")=="True"):
                        dict["site_link"] = "/movie_info/" + dict.get("imdbID")
                        list.append(dict)
        except KeyError as e:
            print("tastedive not working")
    except urllib.error.HTTPError as err:
        print("Invalid url request, something went wrong" )
        list=[]
    return list

def name_from_id(id):
    '''Retrieves movie name based on id'''
    data = movie_info("&i=", id)
    return data.get("Title")
