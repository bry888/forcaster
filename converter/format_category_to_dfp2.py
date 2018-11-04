import urllib.request
import json

def get_rid_of_PL(phrase):
    return phrase.replace('ą','a').replace('ę','e').replace('ó','o').replace('ż','z').replace('ź','z').replace('ś','s').replace('ń','n').replace('ł','l').replace('ć','c')

def load_service_json(param):
    with urllib.request.urlopen(param) as response:
        html = response.read().decode('utf-8')
        return json.loads(html)


def convert_urls_for_dfp(links):
    links_list = links.strip().split('\r\n') # <-- potrzebne w textarea!!!
    if links_list != ['']:

        some_link = 'http://sth='

        try:
            wynik = 0
        except:
            error = url + ' is not a valid category link'
            return (None, error)

        return (wynik, None)
        # (wynik , ERROR_if_one_raised)

    else:
        return 'Paste links to convert them'
