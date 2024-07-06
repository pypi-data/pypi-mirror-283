import requests, error_handler

class WhatPulse:
    def __init__(self, port, retrieve, auto_setup: bool) -> None:
        self.port = port
        self.dataset = dict()
        self.retrieve = retrieve
        self.url_to_api = f"http://localhost:{port}/v1/{retrieve}"
        self.auto_setup = auto_setup

        if auto_setup == True:
            self.setup_api(retrieve)
        elif auto_setup == False:
            pass
        else:
            error_handler.wrong_type(self.retrieve)

    def setup_api(self, retrieve: str):
        push = ["pulse", "open-window", "profiles/activate"]
        get = ["account-totals", "realtime", "unpulsed", "all-stats", "profiles"]

        if retrieve in get:
            rsp = requests.get(self.url_to_api)
        elif retrieve in push:
            rsp = requests.post(self.url_to_api)
        else:
            error_handler.request_type_not_found()
        
        self.dataset = rsp.json(); self.retrieve = retrieve
        return self.dataset
    
    def return_ranks_location(self):
        ranks = None
        try:
            if self.retrieve == "account-totals":
                ranks = self.dataset["ranks"]
            
            elif self.retrieve == "all-stats":
                ranks = self.dataset["account-totals"]["ranks"]
        except:
            error_handler.not_initated()
        return ranks


    def return_all_keys_values(self):
        '''
        Works for:
            account-totals
            realtime
            unpulsed
            all-stats
            profiles
        '''
        try:
            all_keys = list(self.dataset.keys())
        except:
            error_handler.not_initated()
        
        all_values = list()
        for key in self.dataset.keys():
            all_values.append(self.dataset[key])
        
        return list(all_keys), all_values

    def return_value(self, key):
        '''
        Works for:
            account-totals
            realtime
            unpulsed
            all-stats
            profiles
        '''
        try:
            value = self.dataset[key]
            return value
        except:
            error_handler.key_not_found()
    
    def return_all_ranks(self):
        '''
        Works for:
            account-totals
            all-stats
        '''
        ranks = self.return_ranks_location()

        keys = list(ranks.keys())
        
        all_ranks = []
        all_ranks_formatted = list()

        for i in range(len(keys)):
            if i % 2 == 0:
                all_ranks.append((keys[i], ranks[keys[i]]))
            else:
                all_ranks_formatted.append((keys[i], ranks[keys[i]]))
        
        return all_ranks, all_ranks_formatted

    def return_rank(self, key: str):
        '''
        Works for:
            account-totals
            all-stats
        '''
        ranks = self.return_ranks_location()
        try:
            value = ranks[key]
            return value
        except:
            error_handler.key_not_found()