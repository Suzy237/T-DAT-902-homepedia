import requests
from lxml import etree
import time

def scrapping_page_link(response):
    # Vérifier que la requête a réussi
    if response.status_code == 200:
        # Parser le contenu HTML de la page avec lxml
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.content, parser)

        # Trouver les liens dans le tableau avec XPath
        mv_table_link = tree.xpath('//tbody//a/@href')
        #print(mv_table_link)
        if mv_table_link!=[]:
            #print(mv_table_link)
            return [link.replace('avis.html', '').strip() for link in mv_table_link]
        else :
            mv_table_link='Stop'
            return mv_table_link
                        

def all_site_page_link(url, link_table):
    response = requests.get(url)
    indentation_page = 2
    link_table = scrapping_page_link(response)
    print(link_table[-1])
    try:
        while link_table[-1]!="STOP":
            url_next_page = url + f'?page={indentation_page}'
            response = requests.get(url_next_page)
            link_table.extend(scrapping_page_link(response))
            indentation_page += 1
        
    except Exception as e:
        print(f"An error occurred: {e}")

    return list(set(link_table))

def mainScrapping(home="https://www.bien-dans-ma-ville.fr/classement-ville/"):
    link_table = []
    debut = time.time()
    var = all_site_page_link(home, link_table=link_table)
    fin = time.time() - debut
    print(f"{int(fin)} secondes {len(var)}")

    return var

if __name__ == '__main__':
    mainScrapping()
