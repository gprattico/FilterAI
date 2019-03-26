from Parser.Parser import Parser
import os, re

def main():

    print('hello')

    trainAI()


def trainAI():

    parser = Parser('./data/train')

    directoryList = parser.listAllInDirectory()

    #print(os.scandir('./data/train'))

    for file in os.scandir('./data/train'):
        f = open(file,'r')
        lst = (re.split('\[\^a-zA-Z\]', f.read()))[0].split(" ")
        print(lst)
        break


    # string = 'well hello there'
    # words = re.split('\[\^a-zA-Z\]', string)
    # string2 = string.split(" ")
    # words2 = words[0].split(" ")
    # print(words2)




    




if __name__ == "__main__":
    main()