from Parser.Parser import Parser
import os, re

def main():

    print('hello')

    parser = Parser('./data/train')
    parser.start()

if __name__ == "__main__":
    main()