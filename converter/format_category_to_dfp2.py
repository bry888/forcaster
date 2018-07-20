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

        alias_to_cat = 'http://discovery-proxy.allegrogroup.com/p/category-alias/category-aliases?tree.name=listing-pl&alias='
        kat_dict = 'http://discovery-proxy.allegrogroup.com/p/mskip-service/category-paths?id='
        parents_dict = 'http://discovery-proxy.allegrogroup.com/p/mskip-service/categories?parent.id='
        home = '954b95b6-43cf-4104-8354-dea4d9b10ddf'
        home_dict = parents_dict + home

        # build dict Kategorie Działów
        j = load_service_json(home_dict)
        home_dict = dict([ (get_rid_of_PL((i['name']).lower().replace(' ', '-')), i['id']) for i in j['categories'] ])

        cat_list = []
        nums = []

        try:
            for url in links_list:
                if 'dzial' in url:
                    parent = home_dict[url[url.rfind('/')+1:]]

                    if parent.isnumeric():
                        cat_list.append(parent)
                    else:
                        j = load_service_json(parents_dict+parent)
                        cat_list += [ i['id'] for i in j['categories'] ]

                else:
                    url = url.split('?')[0]
                    num = url[url.rfind('-')+1:]
                    if num.isnumeric(): # listing with id in url
                        nums.append(num)
                    else: # no id in url
                        j = load_service_json(alias_to_cat+url[url.rfind('/')+1:])
                        cat_list.append(j['category']['id'])

            # build category chains from lower path categories
            if nums != []:
                j = load_service_json(kat_dict + ','.join(nums))
                cat_list += [ '_'.join([ i['id'] for i in p['path'] if i['id'].isnumeric() ]) for p in j['paths'] ]

        except:
            error = url + ' is not a valid category link'
            return (None, error)

        return (','.join([ i+','+i+'_*' for i in cat_list ]), None)
        # (10_717_257732_*,10_717_257732,11763_*,11763 , ERROR_if_one_raised)

    else:
        return 'Paste links to convert them'
