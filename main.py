from Parser import Parser
import os

def main():

    print('hello')

    trainAI()


def trainAI():

    parser = Parser('./data/train')

    directoryList = len(parser.listAllInDirectory())
    print('The length of directory is \n'+str(directoryList))

    




if __name__ == "__main__":
    main()