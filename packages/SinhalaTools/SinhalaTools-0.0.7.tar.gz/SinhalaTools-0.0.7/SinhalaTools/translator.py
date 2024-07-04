import requests
import re
import os
import html

import concurrent.futures
import urllib.parse


def make_request(target_language, source_language, text, timeout):
    escaped_text = urllib.parse.quote(text.encode('utf8'))
    url = 'https://translate.google.com/m?tl=%s&sl=%s&q=%s' % (
        target_language, source_language, escaped_text)
    response = requests.get(url, timeout=timeout)
    result = response.text.encode('utf8').decode('utf8')
    result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', result)
    if not result:
        print('\nError: Unknown error.')
        f = open('error.txt')
        f.write(response.text)
        f.close()
        exit(0)
    return html.unescape(result[0])


def translate(text, source_language='auto', target_language='si', timeout=5):
    '''
    Translates the text.
    Args:
        text (str): Text to translate
        source_language (str): Source language (default is auto)
        target_language (str): Target language (default is Sinhala)
        timeout (int): Timeout in seconds (default is 5)
    Returns:
        str: Translated text
    '''
    if len(text) > 5000:
        print('\nError: It can only detect 5000 characters at once. (%d characters found.)' % (
            len(text)))
        exit(0)
    if type(target_language) is list:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                make_request, target, source_language, text, timeout) for target in target_language]
            return_value = [f.result() for f in futures]
            return return_value
    return make_request(target_language, source_language, text, timeout)


def translate_file(file_path, source_language='auto', target_language='si', timeout=5):
    '''
    Translates the contents of a file.
    Args:
        file_path (str): Path to the file
        source_language (str): Source language (default is auto)
        target_language (str): Target language (default is Sinhala)
        timeout (int): Timeout in seconds (default is 5)
    Returns:
        str: Translated text
        '''
    if not os.path.isfile(file_path):
        print('\nError: The file or path is incorrect.')
        exit(0)
    f = open(file_path)
    text = translate(f.read(), source_language, target_language, timeout)
    f.close()
    return text
