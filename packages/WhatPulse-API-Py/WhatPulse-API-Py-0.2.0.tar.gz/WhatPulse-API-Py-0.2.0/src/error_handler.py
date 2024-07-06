def not_initated():
    raise NameError("couldn't read any keys from self.dataset... Did you set the dataset up yet?")

def key_not_found():
    raise KeyError("Couldn't find key in your dataset")

def request_type_not_found():
    raise NameError("Get/Post Request Type not found!\nSupported Types:\nPost: 'pulse', 'open-window' or 'profiles/activate'\nGet: 'account-totals', 'realtime', 'unpulsed', 'all-stats' or 'profiles'")

def wrong_type(retrieve):
    raise TypeError(f"auto_setup must be a boolean. Not a/an {type(retrieve)}")