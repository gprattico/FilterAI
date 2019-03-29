import os, re

class Parser:
    def __init__(self, directory):
        self.directory = directory
        self.globalVocab = []
        self.globalVocabHam = []
        self.globalVocabSpam = []
        self.wordsDict = {}
        self.wordsDictHam = {}
        self.wordsDictSpam = {}

    def start(self):

        for file in os.scandir(self.directory):

            f = open(file, 'r')
            vocabTemp = re.split('[^a-zA-Z]', f.read())
            vocabTemp2 = list(filter(('').__ne__, vocabTemp))

            # lowercase for all elements
            fileVocab = [x.lower() for x in vocabTemp2]

            if file.name.split("-")[1] == 'ham':
                self.globalVocabHam = self.mergeVocab(self.globalVocabHam, fileVocab, self.wordsDictHam)
                print('in ham')
                print(self.wordsDictHam)
            else:
                self.globalVocabSpam = self.mergeVocab(self.globalVocabSpam, fileVocab, self.wordsDictSpam)
                print('in spam')
            #self.globalVocab = self.mergeVocab(self.globalVocab, fileVocab, self.wordsDict)

            # print the file name as the program reads the file
            print(file)
            f.close()

        print(self.globalVocab)
        print(self.wordsDict)

    def mergeVocab(self, globalVocab, fileVocab, wordsDict):

        for word in fileVocab:
            if word in globalVocab:
                wordsDict[word] = wordsDict[word] + 1
            else:
                globalVocab.append(word)
                wordsDict[word] = 1

        return globalVocab



