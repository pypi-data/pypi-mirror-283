from .base import Joke
import requests


class A(Joke):

    def get_random_joke(self):
        url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

        querystring = {"format": "json", "contains": "C%23", "idRange": "0-150", "blacklistFlags": "nsfw,racist"}

        headers = {
            "x-rapidapi-key": "7f094253edmsh877aacc1ff2c6c7p1b14a4jsnacaf551915a9",
            "x-rapidapi-host": "jokeapi-v2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring).json()
        return response["setup"] + " \n"+response["delivery"]


class C(Joke):

    def get_random_joke(self):
        url = "https://jokes-always.p.rapidapi.com/common"

        headers = {
            "x-rapidapi-key": "7f094253edmsh877aacc1ff2c6c7p1b14a4jsnacaf551915a9",
            "x-rapidapi-host": "jokes-always.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers).json()

        return response["data"]


class B(Joke):

    def get_random_joke(self):
        url = "https://manatee-jokes.p.rapidapi.com/manatees/random"

        headers = {
            "x-rapidapi-key": "7f094253edmsh877aacc1ff2c6c7p1b14a4jsnacaf551915a9",
            "x-rapidapi-host": "manatee-jokes.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers).json()
        return response["setup"] + " \n"+response["punchline"]

