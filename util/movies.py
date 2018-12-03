import urllib.request, json

#OMDb apikey=1891fe35
#tastedive 324992-SoftdevP-U4MUASLY

def movie_info(parameter, value):
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
    data = json.loads(info)
    return data;

def better_movie_list(old_list):
    list = []
    for movie in old_list:
        dict = movie_info("&i=", movie.get("imdbID"))
        dict["site_link"] = "/movie_info/" + movie.get("imdbID")
        list.append(dict)
    return list
