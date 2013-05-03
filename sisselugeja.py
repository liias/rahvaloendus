# -*- coding: utf-8 -*-
SISENDFAIL = 'data/sisend.prn'

# Puhtalt sisendfailist sisselugemiseks mõeldud klass
class Sisselugeja:
    def __init__(self):
        self.read = None

    def loe_sisse(self):
        with open(SISENDFAIL) as fp:
            self.read = fp.readlines()

    def min(self):
        return self._rea_v22rtus(0)

    def max(self):
        return self._rea_v22rtus(1)

    def kvantide_arv(self):
        return self._rea_v22rtus(2)

    def klastrite_arv(self):
        return self._rea_v22rtus(3)

    def kvandid(self):
        kvantide_list = []
        for rida in self.read[4:]:
            kvantide_list.append(self._tee_reast_kvant(rida))
        return kvantide_list

    # teeb reast pythoni sõnastiku-objekti
    # selline v.b liigne töö / mälukasutus hoiab meie põhiprogrammi sõltumatuna
    # sisendfaili formaadi suhtes
    def _tee_reast_kvant(self, rida):
        # viimasest semikoolonist paremal pool olev reavahetus läheb tühimuutujasse _
        nr, kaal, naabrid_str, _ = rida.split(';')
        return {
            "nr": nr,
            "kaal": kaal,
            "naabrid": [int(n) for n in naabrid_str.split(',')]
        }

    # esimese rea indeks on 0
    def _rea_v22rtus(self, reaindeks):
        return self._v22rtus(self.read[reaindeks])

    # võtab võrdusmärgist paremalt poolt väärtuse ning kustutab tühikud,
    # semikoolonid ning reavahetused
    def _v22rtus(self, rida):
        return int(rida.split('=')[1].strip(' ;\n'))
