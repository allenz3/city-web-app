import urllib.request, urllib.error, urllib.parse, json, webbrowser, api_keys


### Utility functions you may want to use
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


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



def get_photo_ids(text, n):
    flickr_str = flickrREST(params={'text': text, 'per_page': n}).read()
    flickr_data = json.loads(flickr_str)
    id_list = []

    for pic in flickr_data['photos']['photo']:
        id_list.append(pic['id'])

    if len(id_list) == 0:
        return None

    return id_list



def get_photo_info(photoid):
    flickr_str = flickrREST(method='flickr.photos.getInfo', params={'photo_id': photoid}).read()
    flickr_data = json.loads(flickr_str)
    if len(flickr_data) == 0:
        return None
    return flickr_data


class Photo():
    """A class to represent a photo from Flickr"""

    def __init__(self, photo_dictionary):
        self.title = photo_dictionary['photo']['title']['_content']
        self.author = photo_dictionary['photo']['owner']['username']
        self.userid = photo_dictionary['photo']['owner']['nsid']
        self.tags = [x['_content'] for x in photo_dictionary.get('photo').get('tags').get('tag')]
        self.comment_count = int(photo_dictionary['photo']['comments']['_content'])
        self.num_views = int(photo_dictionary['photo']['views'])
        self.url = photo_dictionary.get('photo').get('urls').get('url')[0]['_content']
        self.farm = int(photo_dictionary['photo']['farm'])
        self.server = int(photo_dictionary['photo']['server'])
        self.id = int(photo_dictionary['photo']['id'])
        self.secret = photo_dictionary['photo']['secret']


    def make_photo_url(self, size='q'):
        baseurl = 'https://live.staticflickr.com/{server_id_param}/{photo_id_param}_{secret_param}_{size_letter}.jpg' \
            .format(server_id_param=self.server, photo_id_param=self.id, secret_param=self.secret, size_letter=size)
        return baseurl


    def __str__(self):
        result = '~~~ {photo_title_param} ~~~ \n author: {author_param} \n number of tags: {num_tags_param} \n views: {views_param} \n comments: {comments_param} \n url: {url_param}' \
            .format(photo_title_param=self.title, author_param=self.author, num_tags_param=len(self.tags),
                    views_param=self.num_views, comments_param=self.comment_count, url_param=self.url)
        return result



