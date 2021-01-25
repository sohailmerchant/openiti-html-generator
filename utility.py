import os
import urllib.request
import json, csv
import openiti

path = r"/mnt/c/Development Work/0400AH/data/"

def get_book_files(path):

    for root, dirs, files in os.walk(path):
        dir_name = root.split('/')[-2]
        for name in files:
            if not (name.endswith('.yml') or name.endswith('.md')):
                print(root+'/'+name)

#get_book_files(path)

def get_book_metadata(book_id):
    """Get metadata of the book by book Id

    Args:
    s (str): Book Id e.g. 'JK000001'
    """
    file = 'metadata.csv'
    with open(file, encoding='utf-8') as f:
        rd = csv.DictReader(f,delimiter="\t")
        for dct in map(dict, rd):
            if book_id == dct['id']:
                return dct

#a = get_book_metadata('SAWS20200409')
#print(a)

