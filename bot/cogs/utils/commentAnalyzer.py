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
                     'requestedAttributes': {'TOXICITY': {}}}
        response = self._send_request(data)
        return response

    def get_severe_toxicity(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise  Exception("Invalid Language for Severe toxicity report")
        data = {'comment': {'text': comment},
                    'languages': [language],
                    'requestedAttributes': {'SEVERE_TOXICITY': {}}}
        response = self._send_request(data)
        return response

    def get_ltr(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise  Exception("Invalid Language for Likely to Reject report")
        data = {'comment': {'text': comment},
                    'languages': [language],
                    'requestedAttributes': {'SEVERE_TOXICITY': {}}}
        response = self._send_request(data)
        return response

    def get_incoherent(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for incoherence report")
        data = {'comment': {'text': comment},
                    'languages': [language],
                    'requestedAttributes': {'INCOHERENT': {}}}
        return self._send_request(data)

    def get_insult(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for insult report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {'INSULT': {}}}
        return self._send_request(data)

    def get_threat(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for threat report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {'THREAT': {}}}
        return self._send_request(data)

    def get_spam(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for spam report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {'SPAM': {}}}
        return self._send_request(data)

    def get_profanity(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for profanity report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {'PROFANITY': {}}}
        return self._send_request(data)

    def get_se_report(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for sexually explicit report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {'SEXUALLY_EXPLICIT': {}}}
        return self._send_request(data)

    def get_obscene(self, comment, language='en'):
        languages = ['en']
        if language not in languages:
            raise Exception("Invalid Language for obscene report")
        data = {'comment': {'text': comment},
                'languages': [language],
                'requestedAttributes': {'OBSCENE': {}}}
        return self._send_request(data)

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

#

#
#     def _send_request(self, data):
#         r = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
#                         params=self.payload,
#                         headers=self.headers,
#                             json=data)
#         if r.status_code != 200:
#             raise Exception("Error Making Your Request")
#         return json.loads(r.text)
