from Parser.Parser import Parser
import os, re

def main():

    print('hello')

    trainAI()


def trainAI():

    parser = Parser('./data/train')

    globalVocab = []

    for file in os.scandir('./data/train'):
        f = open(file,'r')
        #vocabTemp = (re.split('[^a-zA-Z]', f.read()))[0].split(" ")
        vocabTemp = re.split('[^a-zA-Z]', f.read())
        vocabTemp2 = list(filter(('').__ne__, vocabTemp))

        #lowercase for all elements
        fileVocab = [x.lower() for x in vocabTemp2]

        print(fileVocab)

        globalVocab = mergeVocab(globalVocab, fileVocab)

        #print the file name as the program reads the file
        print(file)
        f.close()

    print(globalVocab)

def mergeVocab(globalVocab, fileVocab):

    for word in fileVocab:
        if word in globalVocab:
            pass
        else:
            globalVocab.append(word)

    return globalVocab

if __name__ == "__main__":
    main()