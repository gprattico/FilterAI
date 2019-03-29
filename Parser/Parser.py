import os, re

class Parser:
    def __init__(self, directory):
        self.directory = directory
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
                self.wordsDictHam = self.mergeVocab(self.wordsDictHam, fileVocab)
                print('processing as ham')
            else:
                self.wordsDictSpam = self.mergeVocab(self.wordsDictSpam, fileVocab)
                print('processing as spam')

            # print the file name as the program reads the file
            print(file)
            f.close()

        self.checkForZeroFrequencyWords(self.wordsDictHam, self.wordsDictSpam)

        print('DONE')


    def mergeVocab(self, wordsDict, fileVocab):

        for word in fileVocab:
            if word in wordsDict:
                wordsDict[word]['frequency'] = wordsDict[word]['frequency'] + 1
            else:
                wordsDict[word] = {'frequency': 1}

        return wordsDict

    def checkForZeroFrequencyWords(self,wordsDictHam, wordsDictSpam):

        #add any word from ham dict to spam dict if spam doesnt have it
        for key in wordsDictHam:
            if key not in wordsDictSpam:
                wordsDictSpam[key] = {'frequency': 0}

        #add any words in spam dict to ham dict if ham doesnt it
        for key in wordsDictSpam:
            if key not in wordsDictHam:
                wordsDictHam[key] = {'frequency': 0}




