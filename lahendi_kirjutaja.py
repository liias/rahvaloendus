# -*- coding: utf-8 -*-

V2LJUNDFAIL = 'data/klastrid.prn'

# Lahendiks on tekstifail klastrid.prn: klastri number ja komponentide loetelu
# 1;12,15,7,11,14,16,2,3,4,1;
# 2;13,9,8,5,6,10;


class LahendiKirjutaja:
    def _tee_faili_sisu(self, klastrid):
        faili_sisu = ""
        for i, klaster in enumerate(klastrid, start=1):
            faili_sisu += "%d;%s;\n" % (i, klaster.v2ljund())
        return faili_sisu

    def kirjuta(self, klastrid):
        with open(V2LJUNDFAIL, 'w') as f:
            v2ljund = self._tee_faili_sisu(klastrid)
            print v2ljund
            read_data = f.write(v2ljund)