import requests
import json

class Predictor():
    def __init__(self):
        self.payload = {'key': ''}
        self.headers = {'Content-Type': 'application/json'}

    def get_toxicity(self, comment, language='en'):
        languages = ['en', 'fr', 'es']
        if language not in languages:
            raise Exception("Invalid Language for toxicity report")
        data = {'comment': {'text': comment},
                     'languages': [language],
                     'requestedAttributes': {'TOXICITY': {}}}
        return self._send_request(data)


    def _send_request(self, data):
        r = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                        params=self.payload,
                        headers=self.headers,
                            json=data)
        if r.status_code != 200:
            raise Exception("Error Making Your Request")
        return json.loads(r.text)
