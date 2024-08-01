#!/usr/bin/python
import argparse
import csv
import logging
import os
import shutil
import sys
import textwrap
from utils.summarize import summarize
import validators

def parse_args(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            A command line utility for website summarization.
            -----------------------------------------------
            These are common commands for this app.'''))
    parser.add_argument(
        'action',
        help='This action should be summarize or bulk')
    parser.add_argument(
        '--url',
        help='A link to the website url'
    )
    parser.add_argument(
        '--sentence',
        help='Argument to define number of sentences for the summary',
        type=int,
        default=2)
    parser.add_argument(
        '--language',
        help='Argument to define language of the summary',
        default='English')
    parser.add_argument(
        '--path',
        help='Path to csv file')

    return parser.parse_args(argv[1:])


def readCsv(path):
    print('\n\n Processing CSV file \n\n')
    sys.stdout.flush()
    data = []
    try:
        with open(path, 'r') as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                data.append(row)
    except:
        with open(path, 'r', encoding="mbcs") as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                data.append(row)
    return data


def writeCsv(data, LANGUAGE, SENTENCES_COUNT):
    print('\n\n Updating CSV file \n\n')
    sys.stdout.flush()
    with open('beneficiary.csv', 'w', newline='') as newFile:
        newFileWriter = csv.writer(newFile)
        length = len(data)
        position = data[0].index('website')
        for i in range(1, length):
            if i == 1:
                _data = data[0]
                _data.append("summary")
                newFileWriter.writerow(_data)
            try:
                __data = data[i]
                url = data[i][position]
                if not validators.url(url):
                    url = 'http://' + url
                if validators.url(url):
                    summary = summarize(url, LANGUAGE, SENTENCES_COUNT)
                    __data.append(summary)
                else:
                    __data.append("Invalid URL")
                newFileWriter.writerow(__data)
            except Exception as e:
                print(f'\n\n Error Skipping line: {e} \n\n')
                sys.stdout.flush()


def processCsv(path, LANGUAGE, SENTENCES_COUNT):
    try:
        print('\n\n Processing Started \n\n')
        sys.stdout.flush()
        data = readCsv(path)
        writeCsv(data, LANGUAGE, SENTENCES_COUNT)
    except Exception as e:
        print(f'\n\n Invalid file in file path: {e} \n\n')
        sys.stdout.flush()


def main(argv=sys.argv):
    logging.basicConfig(filename='applog.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(levelname)s:%(message)s')
    args = parse_args(argv)
    action = args.action
    url = args.url
    path = args.path
    LANGUAGE = args.language
    SENTENCES_COUNT = args.sentence

    if action == 'bulk':
        if path is None:
            print('\n\n Invalid Entry! Please ensure you enter a valid file path \n\n')
            sys.stdout.flush()
            return
        try:
            processCsv(path, LANGUAGE, SENTENCES_COUNT)
        except Exception as e:
            print(f'\n\n Invalid Entry! Please ensure you enter a valid file path: {e} \n\n')
            sys.stdout.flush()
        print('Completed')
        sys.stdout.flush()
        if os.path.isfile('beneficiary.csv'):
            shutil.move('beneficiary.csv', path)
        return
    elif action == 'simple':
        if not validators.url(url):
            print('\n\n Invalid Entry! Please ensure you enter a valid web link \n\n')
            sys.stdout.flush()
            return
        try:
            print(f'\n\n Summarizing URL: {url} \n\n')
            summary = summarize(url, LANGUAGE, SENTENCES_COUNT)
            print(summary)
        except Exception as e:
            print(f'\n\n Invalid Entry! Error processing URL: {e} \n\n')
            sys.stdout.flush()
        print('Completed')
        sys.stdout.flush()
    else:
        print('\nAction command is not supported\n For help: run python app.py -h')
        sys.stdout.flush()
        return


if __name__ == '__main__':
    main()
