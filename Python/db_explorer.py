# Python imports
import re
import copy
import json
import requests
import unicodedata
import csv
import pandas as pd
# Library imports
from bs4 import BeautifulSoup

import os
import mysql.connector as database


class Linnaeus_migration():

    def __init__(self):

        API_URL = "http://127.0.0.1:5003"

        SQL_CONNECTION = database.connect(
            user='admin',
            password=':D',
            host='localhost',
            database="linnaeus")

        CURSOR = SQL_CONNECTION.cursor()

    def get_sql_data(self, table):
        data_list = []
        
        try:
            statement = "SELECT * FROM {0}".format(table)
            self.CURSOR.execute(statement)
            for taxon in self.CURSOR:
                _id = taxon[0]
                project_id = taxon[1]
                taxon_name = taxon[2]
                parent_id = taxon[4]
                rank_id = taxon[5]
                taxon_order = taxon[6]
                
                common_name = ''

                try:
                    common_name = re.search(r'\((.*?)\)',taxon_name).group(1)
                except:
                    pass

                taxon_name = taxon_name.split('(')[0].strip()

                print(_id, project_id, parent_id, rank_id)
                print(taxon_name, common_name, taxon_order, '\n')

                data = {
                    'taxon_id' : _id,
                    'project' : project_id,
                    'name' : taxon_name,
                    'parent' : parent_id,
                    'rank' : rank_id,
                    'order' : taxon_order,
                    'common_name' : common_name            
                }

                data_list.append(data)


                # exit(0)


                # exit(0)
        except database.Error as e:
            print(f"Error retrieving entry from database: {e}")

        return data_list




if __name__ == "__main__":
    lm = Linnaeus_migration()

    data_list = lm.get_sql_data(table='taxa')
    function_path = "/taxon/create"
    request_url = lm.API_URL + function_path

    for data in data_list:
        r = requests.post(request_url, json=data)

    data_list = lm.get_sql_data(table='projects')
    function_path = "/project/create"
    request_url = lm.API_URL + function_path

    for data in data_list:
        r = requests.post(request_url, json=data)