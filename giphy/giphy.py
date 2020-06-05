import json
import re
import os

class giphy(object):
    ''' This library will allow users to add, remove and display from a list of giphy images.'''
    def __init__(self, giphyinv):
        ''' giphyinv is an inventory file that will be used for giphy mapping. '''
        self.giphyinv = giphyinv
        # Check if file exists, if it does not create a new empty JSON
        if os.path.isfile(self.giphyinv):
            self.__load_json()
        else:
            with open(self.giphyinv, "w") as jsonFile:
                jsonFile.write(json.dumps({}))
            self.__load_json()

    def __load_json(self):
        with open (self.giphyinv, "r") as jsonFile:
            self.data = json.load(jsonFile)

    def __save_json(self):
        with open (self.giphyinv, "w") as jsonFile:
            json.dump(self.data, jsonFile)

    def add_giphy(self, name, link):
        self.data[name] = link
        self.__save_json()

    def list_giphy(self):
        giphyitems = ""
        for item in self.data:
            if len(giphyitem) > 1800:
                break
            else:
                giphyitems += item + ", "
        return giphyitems[:-2]

    def remove_giphy(self, name):
        if name in self.data:
            self.data.pop(name)
            self.__save_json()

    def search_giphy(self, name):
        giphyitems = ""
        for item in self.data:
            if len(giphyitem) > 1800:
                break
            else:
                match = re.search(name, item)
                if match.group(0):
                    giphyitems += match.group(0) + ", "
        return giphyitems[:-2]

    def get_giphy(self, name):
        return self.data[name]
