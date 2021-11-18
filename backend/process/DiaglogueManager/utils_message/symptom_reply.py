from backend.config.regrex import *
import regex as re

def diagnose(text, last_request, last_infor):
    tree_diagnose = {
        0 : {
            1: "request_symptom_test_type",
            0: "request_symptom_been_covidarea"
        },
        1: {
            "test_type": "request_symptom_result_test",
            "been_covidarea": {
                1: "inform_high_prop",
                0: "request_symptom_close_f"
            }
        },
        2: {
            "result_test": {
                "pos": {
                    "pt-pcr": "inform_serious_prop",
                    "test-nhanh": "inform_high_prop"
                },
                "neg": {
                    "pt-pcr": "inform_low_prop",
                    "test-nhanh": "request_symptom_been_covidarea"
                }
            },
            "close_f": {
                1: "inform_high_prop",
                0: "inform_low_prop"
            }
        },
        3: {
            1: "inform_high_prop",
            0: "request_symptom_close_f"
        },
        4: {
            1: "inform_high_prop",
            0: "inform_low_prop"
        }
    }
    res = {}
    res_code = ''
    agree = 0 if re.search(disagree_reg, text) else 1
    pos = 'pos' if re.search(pos_reg,text) else 'neg'
    
    degree = last_infor["diagnose"]["tree_degree"]
    if degree in [0,3,4]:
        last_infor['diagnose'][re.sub('request_symptom_','',last_request)] = agree
        res_code = tree_diagnose[degree][agree]
    elif degree == 2:
        if "result_test" in last_request:
            last_infor['diagnose']['result_test'] = pos
            res_code = tree_diagnose[degree]["result_test"][pos][last_infor['diagnose']['covid_test']]
        else:
            res_code = tree_diagnose[degree]["close_f"][agree]
    else:
        if "test_type" in last_request:
            if re.search(r't[e|é][s|t]*\s*nha[n|]h',text):
                last_infor['diagnose']['covid_test'] = 'test-nhanh'
            else:
                last_infor['diagnose']['covid_test'] = 'pt-pcr'
                
            res_code = tree_diagnose[degree]["test_type"]
        else:
            last_infor['diagnose']['been_covidarea'] = agree
            res_code = tree_diagnose[degree]["been_covidarea"][agree]
    
    
    last_infor["diagnose"]["tree_degree"] += 1
    res[res_code] = last_infor
    return res
    

def symptom_rep(text, intent, last_req, last_infor):
    res = {}
    res_code = ''
    print('\t\t------------------TƯ VẤN TRIỆU CHỨNG-------------------')
    if 'symptoms_info' in intent:
        res_code = 'inform_symptoms_info'
    else:
        if 'request_symptom' in last_req:
            return diagnose(text, last_req, last_infor)
        else:
            lst_sym = []
            for intensity_sym in symptom_list:
                for sym in symptom_list[intensity_sym]:
                    if re.search(sym, text):
                        lst_sym.append(re.findall(sym,text)[0])
                        symp = symptom_list[intensity_sym][sym]
                        if last_infor['symptom'][symp]=='':
                            last_infor['symptom'][symp] = 1
                        last_infor['diagnose'][intensity_sym] = 1
                        
            last_infor['diagnose']["tree_degree"] = 0
            if last_infor['diagnose']['serious_symptom']:
                res_code = 'inform_first_serious_symptom/' + ','.join(lst_sym) + '-inform_high_prop'
            else:
                res_code = 'inform_first_normal_symptom/'+','.join(lst_sym) +'-request_symptom_covid_test'
                    
    res[res_code] = last_infor
    return res