import urllib.request, json

#OMDb apikey=1891fe35

def movie_dict():
    url_object = urllib.request.urlopen("http://www.omdbapi.com/?t=john+wick&apikey=1891fe35")
    print("-------------------------\n")
    print(url_object)
    print("-------------------------\n")
    info = url_object.read()
    print("-------------------------\n")
    print(info)
    print("-------------------------\n")
    dict = json.loads(info)
    return dict;
        


