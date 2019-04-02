import os, re, copy, math

class Parser:
    def __init__(self, directory):
        self.directory = directory
        self.wordsDictHam = {}
        self.wordsDictSpam = {}
        self.totalWordsHam = 0
        self.totalWordsSpam = 0
        self.VocabSizeSmoothed = 0
        self.smoothedHamDict = {}
        self.smoothedSpamDict = {}
        self.totalEmailsHam = 0
        self.totalEmailsSpam = 0

    def train(self):

        for file in os.scandir(self.directory):

            f = open(file, 'r', encoding='utf8', errors='replace')
            vocabTemp = re.split('[^a-zA-Z]', f.read())
            vocabTemp2 = list(filter(('').__ne__, vocabTemp))

            # lowercase for all elements
            fileVocab = [x.lower() for x in vocabTemp2]

            if file.name.split("-")[1] == 'ham':
                self.wordsDictHam = self.mergeVocab(self.wordsDictHam, fileVocab)
                self.totalWordsHam = self.totalWordsHam + len(fileVocab)
                self.totalEmailsHam += 1
                print('processing as ham')
            else:
                self.wordsDictSpam = self.mergeVocab(self.wordsDictSpam, fileVocab)
                self.totalWordsSpam = self.totalWordsSpam + len(fileVocab)
                self.totalEmailsSpam+= 1
                print('processing as spam')

            # print the file name as the program reads the file
            print(file)
            f.close()

        #check for 0 frequency words
        self.checkForZeroFrequencyWords(self.wordsDictHam, self.wordsDictSpam)
        print('Frequencies obtained, generating probabilities...')

        #compute probabilities
        self.computeProbabilities(self.wordsDictHam, self.wordsDictSpam)

        print('ham vocab size' + str(len(self.wordsDictHam)))
        print('spam vocab size' + str(len(self.wordsDictSpam)))

        #compute smoothing
        self.addSmoothing(0.5, self.wordsDictHam, self.wordsDictSpam)

        # print('pre smoothed frequency and prob:'+str(self.wordsDictHam['return']['frequency'])+' '+str(self.wordsDictHam['return']['probability']))
        # print('post smoothed frequency and prob:' + str(self.smoothedHamDict['return']['frequency']) + ' ' + str(self.smoothedHamDict['return']['probability']))
        # print(str(self.VocabSizeSmoothed))

        filename = 'model.txt'
        self.writeToFile(filename)

        #classify each test email
        #self.classifyEmails()

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

    def computeProbabilities(self, wordsDictHam, wordsDictSpam):

        for word in wordsDictHam:
            wordsDictHam[word]['probability'] = wordsDictHam[word]['frequency']/self.totalWordsHam

        for word in wordsDictSpam:
            wordsDictSpam[word]['probability'] = wordsDictHam[word]['frequency']/self.totalWordsSpam

    def addSmoothing(self, smoothingValue, wordsDictHam, wordsDictSpam):

        #increase the total words in the class
        vocabSize = len(wordsDictHam)
        self.VocabSizeSmoothed = self.totalWordsHam + smoothingValue*vocabSize

        self.smoothedHamDict = copy.deepcopy(self.wordsDictHam)
        self.smoothedSpamDict = copy.deepcopy(self.wordsDictSpam)

        #add smoothing to every word frequency
        for word in self.smoothedHamDict:
            self.smoothedHamDict[word]['frequency'] = self.smoothedHamDict[word]['frequency'] + smoothingValue
            self.smoothedHamDict[word]['probability'] = self.smoothedHamDict[word]['frequency']/self.VocabSizeSmoothed

        for word in self.smoothedSpamDict:
            self.smoothedSpamDict[word]['frequency'] = self.smoothedSpamDict[word]['frequency'] + smoothingValue
            self.smoothedSpamDict[word]['probability'] = self.smoothedSpamDict[word]['frequency']/self.VocabSizeSmoothed

    def writeToFile(self, name):

        #delete the file if it exists
        if os.path.exists(name):
            os.remove(name)

        #open a new one
        f = open(name, "x")

        index = 1
        for key in sorted(self.smoothedHamDict.keys()):

            f.write(str(index)+'  '+str(key)+'  '+str(self.smoothedHamDict[key]['frequency'])+'  '+
                    str(self.smoothedHamDict[key]['probability'])+'  '+str(self.smoothedSpamDict[key]['frequency'])+'  '+
                    str(self.smoothedSpamDict[key]['probability'])+'\r')
            index += 1

        f.close()
        print('Model created.')

    def classifyEmails(self, directory):

        fileDict = {}

        #for every file
        for file in os.scandir(directory):
            print('Classifying '+ str(file))
            #generate word list
            f = open(file, 'r', encoding='utf8', errors='replace')
            vocabTemp = re.split('[^a-zA-Z]', f.read())
            vocabTemp2 = list(filter(('').__ne__, vocabTemp))
            fileVocab = [x.lower() for x in vocabTemp2]

            #for every word, if its in the model, grab its probability
            fileDict[file] = {}
            fileDict[file]['hamProb'] = self.calculateHamProbability(fileVocab)
            fileDict[file]['spamProb'] = self.calculateSpamProbability(fileVocab)
            fileDict[file]['computed'] = 'ham' if fileDict[file]['hamProb'] > fileDict[file]['spamProb'] else 'spam'
            fileDict[file]['actual'] = file.name.split("-")[1]
            fileDict[file]['decision'] = 'right' if fileDict[file]['computed'] == fileDict[file]['actual'] else 'wrong'

        #write to file baseline
        #delete the file if it exists
        name = 'baseline-result.txt'
        if os.path.exists(name):
            os.remove(name)

        #open a new one
        f = open(name, "x")

        index = 1

        for key in fileDict.keys():

            name = key.name
            f.write(str(index)+'  '+str(name)+'  '+str(fileDict[key]['computed'])+'  '+
                    str(fileDict[key]['hamProb'])+'  '+str(fileDict[key]['spamProb'])+'  '+
                    str(fileDict[key]['actual'])+'  '+str(fileDict[key]['decision'])+'\r')
            index += 1

        f.close()
        print('baseline created.')



    def calculateHamProbability(self, vocab):

        score = 0

        for word in vocab:
            if word in self.smoothedHamDict:
                score += math.log10(self.smoothedHamDict[word]['probability'])
            # else:
            #     print('detected word not in vocab.')

        totalEmails = self.totalEmailsHam + self.totalEmailsSpam
        score += math.log10(self.totalEmailsHam/totalEmails)

        return score

    def calculateSpamProbability(self, vocab):

        score = 0

        for word in vocab:
            if word in self.smoothedHamDict:
                score += math.log10(self.smoothedSpamDict[word]['probability'])
            # else:
            #     print('detected word not in vocab.')

        totalEmails = self.totalEmailsHam + self.totalEmailsSpam
        score += math.log10(self.totalEmailsHam/totalEmails)

        return score













