# -*- coding: utf-8 -*-

# Klaster sisaldab Kvante
# kvandid klastris peavad olema sidusad (kvantide naabrite kaudu)
from operator import attrgetter


class Klaster:
    def __init__(self):
        self.nr = None
        self.kaal = 0
        self.kvandid = [] #Kvant objektid

    def lisa_kvant(self, kvant):
        self.kvandid.append(kvant)
        self.kaal += kvant.kaal

    #peab ka kontrollima, et klastri sidusus säiliks
    # tagastab False kui ei säili (ning kvanti ei eemaldata)
    def eemalda_kvant(self, kvant):
        #i = self.kvandid.index(kvant)
        #for i, kvant in enumerate(self.kvandid):

        #võtame kvandi teiste kvantide seast ära
        self.kvandid.pop(self.kvandid.index(kvant))

        #1. kontrollime, et klastri sidusus säiliks
        #k = [x for x in self.kvandid if x.nr == kvandi_nr][0]
        # leiame kõik selle kvandi naabrid, mis on selles klastris
        # ehk kontrollime et selle kvandi kõik naabrid, mis on selles klastris,
        #  omaks veel mõnda selle klastri kvanti naabrina
        for naabri_nr in kvant.kasutatud_naabrite_numbrid:
            for k in self.kvandid:
                if k.nr == naabri_nr:
                    # kontrollime kas selle kvandi naaber omab veel naabreid
                    if set(k.kasutatud_naabrite_numbrid) & set(self.kvantide_numbrid):
                        print "õnneks selle kvandi naabreid on veel selle klastris, %s vs %s" % (
                        k.kasutatud_naabrite_numbrid, self.kvantide_numbrid)
                        self.kaal -= kvant.kaal
                        return True
        self.kvandid.append(kvant)
        return False

    #naabritega tähendab siin, et klastris pole veel kvandil naabrit küljes
    def leia_hea_kvant(self):
        #TODO arvesta kaugus_peakvandist
        #kvant millel on kõige rohkem naabreid juba klastrisse pandud
        a = [x for x in self.kvandid if x.klastrita_naabrite_arv != 0]
        if not a:
            return None


        #    print "klastrita naabrite arv: %d" % k.klastrita_naabrite_arv
        #kvant = min(a)

        kvant = min(a, key=attrgetter('klastrita_naabrite_arv'))

        #võta mingi selle kvandi naaber
        #naabri_nr = self.v6ta_naaber_kvandi_nr(kvant)
        return kvant

    @property
    def kvantide_numbrid(self):
        return [int(k.nr) for k in self.kvandid]

    def v2ljund(self):
        return ','.join(str(k.nr) for k in self.kvandid) + " (%d)" % self.kaal