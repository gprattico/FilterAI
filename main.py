from Parser.Parser import Parser
import os, re

def main():

    print('hello')

    parser = Parser('./data/train')
    parser.train()
    parser.classifyEmails('./data/test')

if __name__ == "__main__":
    main()