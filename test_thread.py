import requests
from bs4 import BeautifulSoup
import json
import aiohttp
import asyncio
from time import time 

from Scapping import mainScrapping

# Définition des fonctions de scraping avec gestion détaillée des erreurs
def find_politic(soup: BeautifulSoup, id_section, services: list[str] = ["tour1", "tour2"]):
    try:
        politic_result = {}
        for service in services:
            politic_html = soup.find("section", id=id_section).find("div", service)
            names_politic = [img['alt'] for img in politic_html.find_all('img') if 'alt' in img.attrs]
            scores_politic = [score.text for score in politic_html.find_all("div", "score")]
            tour_data = {name: scores_politic[index] for index, name in enumerate(names_politic)}
            politic_result[service] = tour_data
        return politic_result
    except Exception as e:
        print(f"Error in find_politic: {e}")
        raise

def text_service_filter(text):
    try:
        special_caract = text.replace("\n\t", " ").replace("\t\n", " ").replace("\n", "").replace("\t", "").replace("[", "").replace(",", "").replace("La poste", "LaPoste")
        return special_caract.split()
    except Exception as e:
        print(f"Error in text_service_filter: {e}")
        raise

def data_service(list_services: list, list_names: list):
    try:
        datadict = {}
        for index, list_name in enumerate(list_names):
            if list_name in list_services[index]:
                my_list_service = list_services[index][1:]
                commerce_dict = {my_list_service[i]: my_list_service[i + 1] for i in range(0, len(my_list_service), 2)}
                datadict[list_name] = commerce_dict
        return datadict
    except Exception as e:
        print(f"Error in data_service: {e}")
        print(f'DataService:{len(list_names)}/{len(list_services)}')
        try:
            return commerce_dict
        except:
            print(e)
            raise

def find_service(soup: BeautifulSoup, id_section):
    try:
        service_html = soup.find("section", id=id_section)
        service_title = [services.text for services in service_html.find_all("h3")]
        service_filter = [text_service_filter(services.text) for services in service_html.find_all("table")]
        service_dictionnary = data_service(service_filter, service_title)
        return service_dictionnary
    except Exception as e:
        print(f"Error in find_service: {e}")
        
        try: 
            print("Continious")
            return service_filter
        except:
            print("Stop")
            raise

def find_stat(soup: BeautifulSoup, id_section, id_div: str = "table", datanames: list[str] = None, specifique: str = 'td'):
    try:
        dictionnay_data = {}
        index = 0
        secu = soup.find("section", id=id_section)
        table_secu = secu.find(id_div).find_all(specifique)
        table_filter = [filter_secu.text.strip() for filter_secu in table_secu]
        if datanames:
            for dataname in datanames:
                dictionnay_data[dataname] = {
                    table_filter[index]: table_filter[index + 1],
                    table_filter[index + 2]: table_filter[index + 3]
                }
                index += 4  # Passer aux éléments suivants de la liste
            return dictionnay_data
        else:
            data = {table_filter[i]: table_filter[i + 1] for i in range(0, len(table_filter), 2)}
            return data
    except Exception as e:
        print(f"Error in find_stat: {e}")
        try:
            print("Continious")
            return table_filter
        except:
            print(f"Stop:{secu}")
            raise

def canva_chart(soup: BeautifulSoup):
    try:
        data = {}
        canvas_filter = {}
        list_age = ["0-14", "15-29", "30-44", "45-59", "60-74", "75-89", "90+"]
        list_prof = ["Agriculteur", "Artisans,Comerçants", "Cadres et sup", "Professions intermediaires", "Employe", "Ouvrier", "Retraité", "Autres"]
        list_diplome = ["Sans diplome,CEP", "Brevet,BEPC,DNB", "CAP-BEP", "BAC", "BAC+2", "BAC+3 ou +4", "BAC+5 ou plus"]
        list_menage = ["Couple sans enfant", "Couple avec enfants", "Famille monoparentale", "Colocation/Autre", "Personnes seules"]
        summary = {'chart_age': list_age, 'chart_metier': list_prof, 'chart_diplome': list_diplome, 'chart_menage': list_menage}
        charts = soup.find_all(class_='charts')
        for indentation in range(len(charts)):
            canvas = charts[indentation].find_all("canvas")
            for canva in canvas:
                key = canva["id"]
                value = canva["data-data"]
                data[key] = value
        for key in data.keys():
            canvas_filter[key] = chart_summary(data[key], summary_list=summary[key])
        return canvas_filter
    except Exception as e:
        print(f"Error in canva_chart: {e}")
        raise

def chart_summary(dictionny_chart, summary_list):
    try:
        chart_filter = dictionny_chart.replace('[', '').replace(']', '').split(',')
        chart_age_dict = {age: value + '%' for age, value in zip(summary_list, chart_filter)}
        return chart_age_dict
    except Exception as e:
        print(f"Error in chart_summary: {e}")
        raise

def canva_scrap(soup: BeautifulSoup, filter_by_id: str, datatypes: list[str], datanames: list[str]) -> dict:
    try:
        data = {}
        dictionnary_data = {}
        for index, datatype in enumerate(datatypes):
            stat_from_canva = soup.find(id=filter_by_id)[datatype].replace('[', '').replace(']', '').split(',')
            for i in range(len(stat_from_canva)):
                key = 2006 + i
                value = stat_from_canva[i]
                data[key] = int(value)
            dictionnary_data[datanames[index]] = data
        return dictionnary_data
    except Exception as e:
        print(f"Error in canva_scrap: {e}")
        try:
            return stat_from_canva
        except:
            raise

def stat_population_dict(soup: BeautifulSoup) -> dict:
    try:
        data = {}
        _stat_population = soup.find(class_='bloc_chiffre').find_all('td')
        filter_pop_stat = [pop_stat.text.strip() for pop_stat in _stat_population if pop_stat.text.strip() != 'Classement']
        for i in range(0, len(filter_pop_stat), 2):
            key = filter_pop_stat[i]
            value = filter_pop_stat[i + 1]
            data[key] = value
        return data
    except Exception as e:
        print(f"Error in stat_population_dict: {e}")
        raise

def extract_city_info(soup: BeautifulSoup, dict_main):
    try:
        _ville_departement = soup.find('h1')
        geocoordinates = {
            "latitude": soup.find("main")["data-lat"],
            "longitude": soup.find("main")["data-lon"]
        }
        departement = _ville_departement.find("small").text.strip()
        nom_ville = _ville_departement.text.replace(departement, '').strip()
        _stat_population = stat_population_dict(soup=soup)
        evolution_pop = canva_scrap(soup=soup, filter_by_id="chart_evolution", datatypes=["data-data"], datanames=["chart_evolution"])
        chart = canva_chart(soup=soup)
        secu = find_stat(soup=soup, id_section="securite")
        secu_chart = canva_scrap(soup=soup, filter_by_id="chart_infraction", datatypes=["data-data1", "data-data2", "data-data3", "data-data4"], datanames=["Agressions", "Cambriolages", "Vols", "Stupéfiants"])
        immobilier = find_stat(soup, id_section="immobilier", datanames=["Maison", "Appartement"])
        immo_chart = canva_scrap(soup=soup, filter_by_id="chart_immo_evolution", datatypes=["data-appartement", "data-maison"], datanames=["data-appartement", "data-maison"])
        services = find_service(soup=soup, id_section="services")
        politique = find_politic(soup=soup, id_section="politique")

        dict_main[nom_ville] = {
            "geocoordinates": geocoordinates,
            "departement": departement,
            "nom_ville": nom_ville,
            "stat_population": _stat_population,
            "evolution_pop": evolution_pop,
            "chart": chart,
            "secu": secu,
            "secu_chart": secu_chart,
            "immobilier": immobilier,
            "immo_chart": immo_chart,
            "services": services,
            "politique": politique
        }
        return dict_main
    except Exception as e:
        print(f"Error in extract_city_info: {e}")
        raise

# Fonction pour scraper une seule page
async def scrape_page(session, url, dict_main, failed_urls):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                extract_city_info(soup, dict_main)
            else:
                print(f"Failed to retrieve URL: {url} with status code: {response.status}")
                failed_urls.append(url)
    except Exception as e:
        print(f"Exception occurred for URL: {url} - {e}")
        failed_urls.append(url)

# Fonction principale pour scraper plusieurs pages de manière asynchrone
async def scrape_all_pages(urls):
    dict_main = {}
    failed_urls = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_page(session, url, dict_main, failed_urls) for url in urls]
        await asyncio.gather(*tasks)
    return dict_main, failed_urls


# Liste des URLs à scraper
urls = mainScrapping()

debut=time()
# Lancer le scraping
city_data, failed_urls = asyncio.run(scrape_all_pages(urls))

# Stocker les données dans un fichier JSON
with open('city_data.json', 'w') as f:
    json.dump(city_data, f, indent=4)

# Stocker les URLs échouées dans un fichier JSON
with open('failed_urls.json', 'w') as f:
    json.dump(failed_urls, f, indent=4)

print("Scraping terminé. Les données sont stockées dans 'city_data.json' et les URLs échouées dans 'failed_urls.json'")

print(time()-debut)