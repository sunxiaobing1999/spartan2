import numpy as np
from .._model import Generalmodel
# import spartan2.ioutil as ioutil
from spartan.util.ioutil import saveDictListData, loadDictListData


class IAT(Generalmodel):
    aggiat = {}  # key:user; value:iat list
    user_iatpair = {}  # key:user; value: (iat1, iat2) list
    iatpair_user = {}  # key:(iat1, iat2) list; value: user
    iatpaircount = {}  # key:(iat1, iat2); value:count
    iatcount = {}  # key:iat; value:count

    def __init__(self, aggiat={}, user_iatpair={}, iatpair_user={}, iatpaircount={}, iatcount={}):
        self.aggiat = aggiat
        self.user_iatpair = user_iatpair
        self.iatpair_user = iatpair_user
        self.iatpaircount = iatpaircount
        self.iatcount = iatcount
    def run():
        pass

    def calaggiat(self, aggts):
        'aggts: key->user; value->timestamp list'
        for k, lst in aggts.items():
            if len(lst) < 2:
                continue
            lst.sort()
            iat = np.diff(lst)
            self.aggiat[k] = iat

    def save_aggiat(self, outfile):
        saveDictListData(self.aggiat, outfile)

    def load_aggiat(self, infile):
        self.aggiat = loadDictListData(infile, ktype=str, vtype=int)
    
    "construct dict for iat pair to keys"
    def get_iatpair_user_dict(self):
        for k, lst in self.aggiat.items():
            for i in range(len(lst) - 1):
                pair = (lst[i], lst[i + 1])
                if pair not in self.iatpair_user:
                    self.iatpair_user[pair] = []
                self.iatpair_user[pair].append(k)

    def get_user_iatpair_dict(self):
        for k, lst in self.aggiat.items():
            pairs = []
            for i in range(len(lst) - 1):
                pair = (lst[i], lst[i + 1])
                pairs.append(pair)
            self.user_iatpair[k] = pairs

    def getiatpairs(self):
        xs, ys = [], []
        for k, lst in self.aggiat.items():
            for i in range(len(lst) - 1):
                xs.append(lst[i])
                ys.append(lst[i + 1])
        return xs, ys

    def caliatcount(self):
        for k, lst in self.aggiat.items():
            for iat in lst:
                if iat not in self.iatcount:
                    self.iatcount[iat] = 0
                self.iatcount[iat] += 1

    def caliatpaircount(self):
        for k, lst in self.aggiat.items():
            for i in range(len(lst) - 1):
                pair = (lst[i], lst[i+1])
                if pair not in self.iatcount:
                    self.iatpaircount[pair] = 0
                self.iatpaircount[pair] += 1

    'find users that have pairs in iatpairs'
    def find_iatpair_user(self, iatpairs):
        usrset = set()
        for pair in iatpairs:
            if pair in self.iatpair_user:
                usrlist = self.iatpair_user[pair]
                usrset.update(usrlist)
        return list(usrset)
