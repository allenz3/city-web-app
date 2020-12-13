import urllib.request, urllib.error, urllib.parse, json, webbrowser, api_keys


### Utility functions you may want to use
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def flickrREST(baseurl='https://api.flickr.com/services/rest/',
               method='flickr.photos.search',
               api_key=api_keys.flickr_key,
               format='json',
               params={},
               printurl=False
               ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"] = True
    url = baseurl + "?" + urllib.parse.urlencode(params)
    if printurl:
        print(url)
    return safe_get(url)


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

def get_photo_info(tag, n=100, sort="relevance"):
    r = flickrREST(params={"tags": tag, "per_page": n, "sort": sort})
    requeststr = r.read()
    data = json.loads(requeststr)
    if data.get("stat") == "ok":
        # print(data.get("photos").get("photo"))
        return data.get("photos").get("photo")
    else:
        return {}

# def get_photo_ids(tag, n=100, sort="relevance"):
#     r = flickrREST(params={"tags": tag, "per_page": n, "sort": sort})
#     requeststr = r.read()
#     data = json.loads(requeststr)
#     print(data)
#     if data.get("stat") == "ok":
#         ids = [photo.get("id") for photo in data.get("photos").get("photo")]
#         return ids
#     else:
#         return {}
#
# # print(get_photo_ids("Seattle"))
#
# def get_photo_info(photoid):
#     r = flickrREST(method='flickr.photos.search',
#                    params={"photo_id": photoid})
#     requeststr = r.read()
#     data = json.loads(requeststr)
#     if data.get("stat") == "ok":
#         return data.get("photos").get("photo")
#     else:  # data.get("stat") == "fail"
#         return {}



class Photo():
    """A class to represent a photo from Flickr"""

    def __init__(self, infoDict):
        self.server = infoDict.get("server")
        self.id = infoDict.get("id")
        self.secret = infoDict.get("secret")

    def make_photo_url(self, size="q"):
        if size is None:
            return f"https://live.staticflickr.com/{self.server}/{self.id}_{self.secret}.jpg"
        return f"https://live.staticflickr.com/{self.server}/{self.id}_{self.secret}_{size}.jpg"
