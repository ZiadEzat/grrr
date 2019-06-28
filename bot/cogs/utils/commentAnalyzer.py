import requests
import json


class Predictor():
    def init(self):
        self.payload = {'key': ''}
        self.headers = {'Content-Type': 'application/json'}

    def get_toxicity(self, comment, language='en'):
        languages = ['en', 'fr', 'es']
        if language not in languages:
            raise Exception("Invalid Language for toxicity report")
        data = {'comment': {'text': comment},
                     'languages': [language],
                     'requestedAttributes': {'TOXICITY': {},
                                             'SEVERE_TOXICITY': {},
                                             "LIKELY_TO_REJECT": {},
                                             "SPAM": {},
                                             "THREAT": {},
                                             "INSULT": {},
                                             "PROFANITY": {},
                                             "SEXUALLY_EXPLICIT": {},
                                             "OBSCENE": {}
}}
        response = self._send_request(data)
        return response

    def _send_request(self, data):
        r = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                        params=self.payload,
                        headers=self.headers,
                            json=data)
        if r.status_code != 200:
            raise Exception("Error Making Your Request")
        return json.loads(r.text)

# TODO: Threat, Spam, Identity Attack

# class Predictor():
#     def __init__(self):
#         self.payload = {'key': ''}
#         self.headers = {'Content-Type': 'application/json'}
#
#     def get_toxicity(self, comment, language='en'):
#         languages = ['en', 'fr', 'es']
#         if language not in languages:
#             raise Exception("Invalid Language for toxicity report")
#         data = {'comment': {'text': comment},
#                      'languages': [language],
#                      'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}}
#         return self._send_request(data)
#
#     def get_severe_toxicity(self, comment, language='en'):
#         languages = ['en', 'fr', 'es']
#         if language not in languages:
#             raise Exception("Invalid Language for toxicity report")
#         data = {'comment': {'text': comment},
#                      'languages': [language],
#                      'requestedAttributes': {'SEVERE_TOXICITY': {}}}
#         return self._send_request(data)
#
#     def get_incoherent(self, comment, language='en'):
#         languages = ['en']
#         if language not in languages:
#             raise Exception("Invalid Language for incoherence report")
#         data = {'comment': {'text': comment},
#                     'languages': [language],
#                     'requestedAttributes': {'INCOHERENT': {}}}
#         return self._send_request(data)
#
#     def get_insult(self, comment, language='en'):
#         languages = ['en']
#         if language not in languages:
#             raise Exception("Invalid Language for insult report")
#         data = {'comment': {'text': comment},
#                 'languages': [language],
#                 'requestedAttributes': {'INSULT': {}}}
#         return self._send_request(data)
#
#     def _send_request(self, data):
#         r = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
#                         params=self.payload,
#                         headers=self.headers,
#                             json=data)
#         if r.status_code != 200:
#             raise Exception("Error Making Your Request")
#         return json.loads(r.text)
