import string
import  random
import hashlib


class random_string_generator_c(object):
    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        #return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()    



#ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz
