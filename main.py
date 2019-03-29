from Parser.Parser import Parser
import os, re

def main():

    print('hello')

    parser = Parser('./data/train')
    parser.start()


# def trainAI():
#
#     # parser = Parser('./data/train')
#
#     globalVocab = []
#     # frequency dictionary
#     wordsDict = {}
#
#     for file in os.scandir('./data/train'):
#         f = open(file,'r')
#         #vocabTemp = (re.split('[^a-zA-Z]', f.read()))[0].split(" ")
#         vocabTemp = re.split('[^a-zA-Z]', f.read())
#         vocabTemp2 = list(filter(('').__ne__, vocabTemp))
#
#         #lowercase for all elements
#         fileVocab = [x.lower() for x in vocabTemp2]
#
#         globalVocab = mergeVocab(globalVocab, fileVocab, wordsDict)
#
#         #print the file name as the program reads the file
#         print(file)
#         f.close()
#
#     print(globalVocab)
#     print(wordsDict)
#
# def mergeVocab(globalVocab, fileVocab, wordsDict):
#
#     for word in fileVocab:
#         if word in globalVocab:
#             wordsDict[word] = wordsDict[word] + 1
#         else:
#             globalVocab.append(word)
#             wordsDict[word] = 1
#
#     return globalVocab

if __name__ == "__main__":
    main()