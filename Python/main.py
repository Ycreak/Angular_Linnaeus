# Python imports
import re
import copy
import json
import requests
import unicodedata
# Library imports
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Class imports
from models.database import sandbox

import utilities as util

LINNAEUS_URL = 'https://birds-europe.linnaeus.naturalis.nl/linnaeus_ng/app/views/introduction/topic.php'

def init_driver():
    DRIVER_PATH = './chromedriver'
    options = Options()
    options.headless = True
    DRIVER = webdriver.Chrome(options=options, executable_path=DRIVER_PATH) 
    return DRIVER

def find_between_delimiters(left, right, given_string):
    try :
        regex_pattern = left + '(.+?)' + right
        return re.search(regex_pattern, given_string).group(1)
    except AttributeError:
        # Attribute error is expected if string 
        # is not found between given markers
        pass    

def get_projects_urls():
    
    url = 'https://linnaeus.naturalis.nl/'
    response = requests.post(url)
    soup = BeautifulSoup(response.text, 'html5lib')

    results = soup.find(id="projects")
    
    url_list = []

    for item in results.findAll('li'):

        span = item.find('span').get('onclick')

        # retrieve the url from the span
        new_url = re.findall(r'(https?://\S+)', span)[0]
        new_url = new_url.split("'")[0]
    
        url_list.append((new_url, item.text.strip()))

    return url_list

def get_introduction_entries(project_url):
    sidebar_entry_list = []

    # use selenium to dynamically load the page
    DRIVER.get(project_url)
    try: # check if the webpage dynamically loaded the sidebar
        element = WebDriverWait(DRIVER, 10).until(
            EC.presence_of_element_located((By.ID, "allLookupListCell-1"))
        )
    finally:
        page_source = DRIVER.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        side_menu = soup.find(id="lookup-DialogContent")   
        
        for i in side_menu.findAll('p'):
            sidebar_entry_list.append((i.next, i.attrs['lookupid']))

        return sidebar_entry_list

def get_linnaeus_page_content(url):
    
    DRIVER.get(url)
    try:
        element = WebDriverWait(DRIVER, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "proze"))
        )
    finally:
        page_source = DRIVER.page_source
        soup = BeautifulSoup(page_source, 'lxml') 
        return soup
    
def get_selenium_page_content(url: str, EC_element):
    DRIVER.get(url)
    try:
        element = WebDriverWait(DRIVER, 10).until(
            EC.presence_of_element_located(EC_element)
        )
    finally:
        return BeautifulSoup(DRIVER.page_source, 'lxml')    

def add_introduction_to_database(project_url):
    new_database_entry : list = []
    # retrieve the side bar elements and their IDs
    sidebar_entry_list = get_introduction_entries(project_url)

    # get the content for each sidebar entry
    for sidebar_entry in sidebar_entry_list:

        # per entry, create a content field and fill it
        new_content_entry : dict = {}

        title = sidebar_entry[0]
        lookupid = sidebar_entry[1]

        new_content_entry['id'] = int(lookupid)
        new_content_entry['title'] = str(title.capitalize())

        sub_url = project_url + '/linnaeus_ng/app/views/introduction/topic.php?id=' + str(lookupid)

        # retrieve the content from the page
        soup = get_linnaeus_page_content(sub_url)
        
        content_html = soup.find(id="content")

        new_content_entry['text'] = str(content_html)
        
        new_database_entry.append(new_content_entry)

        print('thinking...')
    
    return new_database_entry

def retrieve_animals_from_index(url, category):
    source_page = get_selenium_page_content(url, (By.CLASS_NAME, "index-entry"))
    # first, find all the urls for the lower taxa pages
    letter_urls = source_page.find_all("a", {"class": "alphabet-letter"})
    urls = []
    for lower_taxa_letter_url in letter_urls:
        urls.append(lower_taxa_letter_url.attrs['href'])
    # we also want a link for the letter A...
    if len(urls) > 0: # check if the taxa category exists
        a_string = urls[0].split('?')[0] + '?&&letter=a'
        urls.insert(0, a_string)


    # now retrieve for all the urls all the animals and their taxon links
    animal_list = []   
    for letter_url in urls:
        # we cant wait for an element, because of the Linneaus programming, so we just wait for n seconds for the page to load
        DRIVER.implicitly_wait(3) # seconds
        DRIVER.get(letter_url)
        soup = BeautifulSoup(DRIVER.page_source, 'lxml')    
        # now retrieve every animal     
        for animal in soup.find_all("a", {"class": "index-entry"}):
            taxon_href = animal.attrs['href']
            name = animal.text
            try :
                marker1 = 'id='
                marker2 = '&'
                regex_pattern = marker1 + '(.+?)' + marker2
                href_id = re.search(regex_pattern, taxon_href).group(1)
            except AttributeError:
                # Attribute error is expected if string 
                # is not found between given markers
                pass

            print(name)
            animal_list.append({
                'taxon_href_id' : int(href_id),
                'taxon_href' : str(taxon_href),
                'animal_name' : str(name),
                'category' : category
            })
        print('\n')
    return animal_list

def add_index_to_database(project_url):

    new_database_entry : list = []

    # https://aetideidae.linnaeus.naturalis.nl/linnaeus_ng/app/views/index/index.php?type=higher

    lower_taxa_url =  project_url + '/linnaeus_ng/app/views/index/index.php'
    higher_taxa_url = project_url + '/linnaeus_ng/app/views/index/index.php?type=higher'
    common_names_url = project_url + '/linnaeus_ng/app/views/index/index.php?type=common'

    new_database_entry += retrieve_animals_from_index(lower_taxa_url, 'lower_taxa')
    new_database_entry += retrieve_animals_from_index(higher_taxa_url, 'higher_taxa')
    new_database_entry += retrieve_animals_from_index(common_names_url, 'common_names')

    # exit(0)
    return new_database_entry

def add_glossary_to_database(url):
    
    glossary_url = url + '/linnaeus_ng/app/views/glossary/contents.php'
    
    source_page = get_selenium_page_content(glossary_url, (By.CLASS_NAME, "index-entry"))
    # first, find all the urls for the lower taxa pages
    letter_urls = source_page.find_all("a", {"class": "alphabet-letter"})
    urls = []
    for letter_url in letter_urls:
        urls.append(letter_url.attrs['href'])

    if len(urls) > 0: # check if the taxa category exists
        a_string = urls[0].split('?')[0] + '?letter=a'
        urls.insert(0, a_string)

    # now retrieve for all the urls all the animals and their taxon links
    glossary_list = []   
    for letter_url in urls:
        # we cant wait for an element, because of the Linneaus programming, so we just wait for n seconds for the page to load
        DRIVER.implicitly_wait(3) # seconds
        DRIVER.get(letter_url)
        soup = BeautifulSoup(DRIVER.page_source, 'lxml')    
        # now retrieve every animal     
        
        content_items = soup.find(id="content")      
        for glossary_item in content_items.find_all("a"):
            glossary_href = glossary_item.attrs['href']
            name = glossary_item.text
            try :
                marker1 = 'id='
                marker2 = '&'
                regex_pattern = marker1 + '(.+?)' + marker2
                href_id = re.search(regex_pattern, glossary_href).group(1)
            except AttributeError:
                # Attribute error is expected if string 
                # is not found between given markers
                pass

            # also get the content
            item_content = get_selenium_page_content(glossary_href, (By.ID, "definition"))
            item_content = item_content.find("div", {"id": "definition"})

            glossary_list.append({
                'taxon_href_id' : int(href_id),
                'taxon_href' : str(glossary_href),
                'glossary_name' : str(name),
                'content' : str(item_content)
            })

    return glossary_list

def add_species_data_to_database():
   
    species_tabs = [
        "&cat=TAB_DESCRIPTION",
        "&cat=CTAB_CLASSIFICATION",
        # "&cat=TAB_NOMENCLATURE",
        # "&cat=CTAB_NAMES",
        # "&cat=CTAB_LITERATURE"
        # "&cat=CTAB_MEDIA"
    ]

    f = open('myfile5.json')
    database = json.load(f)
    
    database = database['1']
    
    animals_list = []

    for index_entry in database['index']:

        new_animal_entry = {}
        index_entry_url = index_entry['taxon_href']

        # First, get the classification information
        classification_url = index_entry_url + '&cat=CTAB_CLASSIFICATION'

        # classification_url = 'https://aetideidae.linnaeus.naturalis.nl/linnaeus_ng/app/views/highertaxa/taxon.php?id=125441&cat=CTAB_CLASSIFICATION&epi=193'

        source_page = get_selenium_page_content(classification_url, (By.ID, "content"))
        item_content = source_page.find("div", {"id": "content"})
        # print(item_content)

        # Find the children       
        children_html = item_content.find('p', attrs = {'style':'margin-top: 25px;'})        
        child_list = []
        try:
            children_html = children_html.find_all("a")
            for child in children_html:
                taxon = ''.join(c for c in child.next_sibling if c not in '[]').strip()
                _id = find_between_delimiters('id=', '&', child.attrs['href'])
                child_name = child.text
                child_list.append({'name': child_name, 'taxon': taxon, '_id':_id})
        except:
            pass

        # Find the parents
        parent_html = item_content.find_all("a")
        # Delete the children (this is so dumb)
        parent_html = parent_html[: len(parent_html) - len(child_list)]

        parent_list = []
        if parent_html:
            for parent in parent_html:
                taxon = ''.join(c for c in parent.next_sibling if c not in '[]').strip()
                _id = find_between_delimiters('id=', '&', parent.attrs['href'])
                parent_name = parent.text
                parent_list.append({'name': parent_name, 'taxon': taxon, '_id':_id})
        # print(parent_list)

        item_itself = parent_list.pop()

        new_animal_entry['name'] = item_itself['name']
        new_animal_entry['taxon'] = item_itself['taxon']
        new_animal_entry['_id'] = item_itself['_id']
        new_animal_entry['parents'] = parent_list
        new_animal_entry['children'] = child_list

        # print(index_entry)

        # get the description too
        description_url = index_entry_url + "&cat=TAB_DESCRIPTION"
        source_page = get_selenium_page_content(description_url, (By.ID, "content"))
        item_content = source_page.find("div", {"id": "content"})

        new_animal_entry['description'] = str(item_content)

        animals_list.append(new_animal_entry)

        print(animals_list)
        # break

    return animals_list

def create_tree_from_animals():
    
    f = open('myfile6.json')
    database = json.load(f)
    
    database = database['1']
    
    tree_list = []

    for animal in database['animals']:
        children = []
        for child in animal['children']:
            children.append(child['name'])
        
        tree_list.append([animal['name'], children])

    print(tree_list)

    return tree_list

    exit(0)

########
# MAIN #
########

id_counter = 0 # to name a db entry

# database stuffs
database = {}

database_entry = {
    'id' : 0,    
    'project_title' : '',
    'project_url' : '',
    'content' : [],
    'index' : {},
}

content_entry = {
    'id' : 0,
    'title' : '',
    'text' : ''
}

# first, create a list of all projects
url_list = get_projects_urls()

# how many projects will we loop over
counter = 0

# init selenium
DRIVER = init_driver()

# scrape data from each project
for project_url, project_title in url_list:
    
    id_counter +=1

    # create a database entry and start populating
    new_sandbox = copy.deepcopy(sandbox)
    # new_sandbox['_id'] = id_counter
    new_sandbox['title'] = project_title
    new_sandbox['url'] = project_url

    # break to cut off program
    counter += 1
    if counter > 1:
        break
    
    # new_sandbox['introduction'] = add_introduction_to_database(project_url)
    # new_sandbox['index'] = add_index_to_database(project_url)
    # new_sandbox['glossary'] = add_glossary_to_database(project_url)

    # new_sandbox['animals'] = add_species_data_to_database()
    new_sandbox['tree'] = create_tree_from_animals()
    # exit(0)

    # add the sandbox to the database
    database[id_counter] = new_sandbox
    pass

DRIVER.quit()

# print(database)

out_file = open("myfile_temp.json", "w")
json.dump(database, out_file, indent = 2)
out_file.close()

exit(0)
