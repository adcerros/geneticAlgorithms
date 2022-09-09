
import requests

chromosome = '0000000000000000000000000000000000000000000000000000000000000011'
url = "http://memento.evannai.inf.uc3m.es/age/test?c="


def my_call(url, chromosome):
    my_request = requests.get(url + chromosome)
    return my_request.text




print("El resultado es:" + my_call(url, chromosome))