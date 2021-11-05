from functools import reduce
import random
import json
import re
import requests
from collections import defaultdict
from backend.process.PretrainedModel import PretrainedModel

def generate_reply_text(self, result, reply_text):
    res_code = list(result.keys())[0]
    suggest_reply = ""
    check_end = False
    
    for idx, res in enumerate(res_code.split('-')):
        if idx>=1:
            suggest_reply += '*'

        if res == 'hello':
            suggest_reply += reply_text['hello']
        if res.startswith('inform_first_symptom/'):
            suggest_reply += reply_text['inform_first_symptom'].format(res.split('/')[1])
        if res.startswith('inform_current_numbers'):
            loc,infected,recovered = res.split('+')[1:]
            suggest_reply += reply_text['inform_current_numbers'].format(loc,infected,recovered)
        if res in ['request_age','request_sex','request_usual_symptom','request_rare_symptom', 'inform_symptoms_info',
                        'request_serious_symptom', 'inform_low_prop', 'inform_high_prop','request_location_contact', 'done',
                        'other', 'again','diagnose','incomming', 'request_covid_infor_chithi']:

            suggest_reply += reply_text[res]
        if res.startswith('inform_covid_infor'):
            if res.startswith('inform_covid_infor_chithi_how'):
                suggest_reply += reply_text['inform_covid_infor_chithi_how'][res.split('+')[-1]]
            else:
                suggest_reply += reply_text[res]
        if res.startswith('inform_precaution'):
            suggest_reply += reply_text[res.split('+')[0]][res.split('+')[1]][res.split('+')[2]]
        if 'inform_contact' in res:
            suggest_reply += reply_text['inform_contact']
            suggest_reply += "*image " + reply_text['contact_list']['tram-y-te'][res.split('+')[-1]]
        if 'vaccine' in res:
            suggest_reply += reply_text[res]
    
    return suggest_reply, result, check_end