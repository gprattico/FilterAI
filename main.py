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
        fileVocab = (re.split('\[\^a-zA-Z\]', f.read()))[0].split(" ")

        globalVocab = mergeVocab(globalVocab, fileVocab)
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