from Parser.Parser import Parser
import os, re

def main():

    print('hello')

    parser = Parser('./data/train')

    parser.taskFlag = 1
    parser.train()
    parser.classifyEmails('./data/test')

    parser.taskFlag = 2
    parser.train()
    parser.classifyEmails('./data/test')

    parser.taskFlag = 3
    parser.train()
    parser.classifyEmails('./data/test')

if __name__ == "__main__":
    main()