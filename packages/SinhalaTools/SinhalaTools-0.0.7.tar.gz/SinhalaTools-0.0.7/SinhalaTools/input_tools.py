import requests


def inputTools(text, itc="si-t-i0-und", num=5):
    '''Converts text to Sinhala using Google Input Tools API
    Args:
        text (str): Text to convert
        itc (str): Input tool code (default is Sinhala)
        num (int): Number of suggestions (default is 5)
        Returns:
        dict: JSON response from the API
        '''
    url = f'https://inputtools.google.com/request?text={text}&itc={itc}&num={num}/&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test'

    response = requests.get(url)

    return response.json()
