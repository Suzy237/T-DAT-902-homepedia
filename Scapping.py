import requests
from bs4 import BeautifulSoup
import time
from collections import Counter

# URL de la page à scraper (à modifier avec l'URL réelle)
#url = 'https://www.ville-ideale.fr/classements.php'
# Envoyer une requête GET pour récupérer le contenu de la page


def scrapping_page_link(response):

    
    # Vérifier que la requête a réussi
    if response.status_code == 200 :

        # Parser le contenu HTML de la page avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver les tables par leurs identifiants 'mv' et 'tabchcrit'
        mv_table_link = [link['href'] for link in soup.find('tbody').find_all("a",href=True)]
        
        return [link.replace('avis.html','').strip() for link in mv_table_link]

def all_site_page_link(url,link_table):
    response = requests.get(url)
    #print(response)
    indentation_page = 2
    link_table=scrapping_page_link(response)
    try:

        while response.status_code==200:
            url_next_page=url+f'?page={indentation_page}'
            #print(f"\033[32m{url_next_page}\033[0m]")
            response=requests.get(url_next_page)
            link_table.extend(scrapping_page_link(response))
            indentation_page += 1
    except :

        return list(set(link_table))

    

def mainScrapping(home="https://www.bien-dans-ma-ville.fr/classement-ville/"):
    link_table=[]
    debut=time.time()
    var=all_site_page_link(home,link_table=link_table)
    fin = time.time() - debut
    print(f"{int(fin)} secondes {len(var)}")

    return var

if __name__ =='__main__':
    mainScrapping()