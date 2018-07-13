import urllib.request
import json
# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def convert_urls_for_dfp(links):

    links_list = links.strip().split('\r\n')
    if links_list != ['']:

        # IP:host:
        #url=$(curl http://discovery.qxlint/services/category-listing/instances/ | jq '.links[0].serviceUri' | sed 's/\"//g')
        script = "http://discovery.qxlint/services/category-listing/instances/"

        with urllib.request.urlopen(script) as response:
            html = response.read().decode('utf-8')
            j = json.loads(html)
            ip_port = j['links'][0]['serviceUri']

        info_link = ip_port+'listing-categories?category.id='

        kat_dict = {'elektronika':['10','2','4','8845','122233','122332'],
                    'moda-i-uroda':['1454','19732','1429'],
                    'moda':['1454','19732'],
                    'uroda-i-zdrowie':['1429','121882','63757'],
                    'dom-i-ogrod':['5','20782','73973'],
                    'dom-i-zdrowie':['5','121882','20782','73973'],
                    'dziecko':['11763'],
                    'kultura-i-rozrywka':['7','9','1','122640','20585','98553'],
                    'sport-i-wypoczynek':['3919','63757','55067'],
                    'motoryzacja':['3'],
                    'kolekcje-i-sztuka':['26013','6','76593'],
                    'firma-i-uslugi':['16696','64477']
                    }



        cat_list = []

        try:
            for url in links_list:
                if 'dzial' in url:
                    cat_list += kat_dict[url[url.rfind('/')+1:]]

                else:
                    if '?' in url:
                        index = url.find('?')
                        num = url[url[:index].rfind('-')+1:index]
                    else:
                        num = url[url.rfind('-')+1:]

                    with urllib.request.urlopen(info_link+num) as response:
                        html = response.read().decode('utf-8')
                        j = json.loads(html)
                        id_list = [i['id'] for i in j['path'] if i['id'].isnumeric()]
                        cat_list.append('_'.join(id_list))

            return (','.join([ i+','+i+'_*' for i in cat_list ]), None)
            # (10_717_257732_*,10_717_257732,11763_*,11763 , ERROR_if_one_raised)

        except:
            error = url + ' is not a valid category link'
            return (None, error)

    else:
        return 'Paste links to convert them'
