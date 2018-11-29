import urllib.request, json

#OMDb apikey=1891fe35

def movie_dict(parameter, value):
    url_stub = "http://www.omdbapi.com/?"
    api_key = "apikey=1891fe35"
    search = parameter + value
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
    dict = json.loads(info)
    return dict;
        


