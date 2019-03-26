import os

class Parser:
    def __init__(self, directory):
        self.directory = directory
        self.vocabulary = []


    def parseFile(self, filename):

        #parse the file
        lst = []

        return lst

    def getVocabulary(self):

        return self.vocabulary

    def listAllInDirectory(self):

        lst = os.listdir(self.directory)

        return lst