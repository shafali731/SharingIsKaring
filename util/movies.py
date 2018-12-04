import urllib.request, json

#OMDb apikey=1891fe35
#tastedive 324992-SoftdevP-U4MUASLY

def remove_nonascii(text):
    text = ''.join(i for i in text if ord(i)<128)
    text = ''.join(i for i in text if i=="%")
    return text

def movie_info(parameter, value):
    url_stub = "http://www.omdbapi.com/?"
    api_key = "apikey=1891fe35"
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
    return data;

def better_movie_list(old_list):
    new_list = []
    if isinstance(old_list, list):
        for movie in old_list:        
            dict = movie_info("&i=", movie.get("imdbID"))
            if (dict.get("Response")=="True"):
                dict["site_link"] = "/movie_info/" + movie.get("imdbID")
                new_list.append(dict)
    return new_list

def movie_rec(movie_name):
    url_stub = "https://tastedive.com/api/similar?"
    api_key = "k=324992-SoftdevP-U4MUASLY"
    parameter = "&q=movie:"
    search = parameter + movie_name
    url = url_stub + api_key + search

    hdr = { 'User-Agent' : 'Mozilla/5.0' }

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
    for movie in data["Similar"]["Results"]:
        if (movie.get("Type")=="movie"):
            movie_title = remove_nonascii(movie.get("Name").replace(" ", "+"))
            dict = movie_info("&t=", movie_title)
            if (dict.get("Response")=="True"):
                dict["site_link"] = "/movie_info/" + dict.get("imdbID")
                list.append(dict)
    return list


