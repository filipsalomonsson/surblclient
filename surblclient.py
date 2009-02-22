#!/usr/bin/env python
"""SURBL checker (http://www.surbl.org/)

Example usage:
>>> from surblclient import surbl
>>> domain = "foo.bar.test.surbl.org"
>>> domain in surbl
True
>>> surbl.lookup(domain)
('test.surbl.org', ['sc', 'ws', 'ph', 'ob', 'ab', 'jp'])
>>> if domain in surbl:
...     print "%s blacklisted in %s" % surbl.lookup(domain)
... 
test.surbl.org blacklisted in ['sc', 'ws', 'ph', 'ob', 'ab', 'jp']
"""

# Copyright (c) 2009 Filip Salomonsson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import socket
from urlparse import urlsplit
import re

VERSION = "0.1"

_flags = ((2, "sc"), (4, "ws"), (8, "ph"), (16, "ob"), (32, "ab"), (64, "jp"))

class Blacklist:
    def __init__(self):
        self._cache = (None, None)

    def _get_base_domain(self, domain):
        # Remove userinfo
        if "@" in domain: domain = domain[domain.index("@")+1:]
        # Remove port
        if ":" in domain: domain = domain[:domain.index(":")]
        # Choose the right "depth"...
        if _two_level_tlds.search(domain): n = 3
        else: n = 2
        return ".".join(domain.split(".")[-n:])

    def _lookup_exact(self, domain):
        """Like 'lookup', but checks the exact domain name given.
        Not for direct use.
        """
        cached_domain, flags = self._cache
        if cached_domain != domain:
            try:
                ip = socket.gethostbyname(domain + ".multi.surbl.org")
                flags = int(ip.split(".")[-1])
            except socket.gaierror, e:
                if e[0] in (socket.EAI_NONAME, socket.EAI_NODATA):
                    # No record found
                    flags = None
                    self._cache = (domain, flags)
                    return False
                else:
                    # Unhandled error, pass test for now
                    return None
            except:
                # Not sure if this can happen. Timeouts?
                return None
            self._cache = (domain, flags)
        if flags:
            return (domain, [s for (n, s) in _flags if flags & n])
        else:
            return False
        

    def lookup(self, domain):
        """Extract base domain and check it against SURBL.
        Return (basedomain, lists) tuple, where basedomain is the
        base domain and lists is a list of strings indicating which
        blacklists the domain was found in.
        If there was no match, return False.
        If unsure (temporary error), return None.
        """
        domain = self._get_base_domain(domain)
        return self._lookup_exact(domain)

    def __contains__(self, domain):
        """Return True if base domain is listed in SURBL;
        False otherwise.
        """
        return bool(self.lookup(domain))
        
_two_level_tlds = re.compile(r"""(?:^|\.)
(?:(?:com|edu|gov|net|mil|org)\.ac
|(?:com|net|org|gov|ac|co|sch|pro)\.ae
|(?:com|org|edu|gov)\.ai
|(?:com|net|org|gov|mil|edu|int)\.ar
|(?:co|ac|or|gv|priv)\.at
|(?:com|gov|org|edu|id|oz|info|net|asn|csiro|telememo|conf|otc|id)\.au
|(?:com|net|org)\.az
|(?:com|net|org)\.bb
|(?:ac|belgie|dns|fgov)\.be
|(?:com|gov|net|edu|org)\.bh
|(?:com|edu|gov|org|net)\.bm
|(?:adm|adv|agr|am|arq|art|ato|bio|bmd|cim|cng|cnt|com|coop|ecn|edu|eng|esp|etc|eti|far|fm|fnd|fot|fst|g12|ggf|gov|imb|ind|inf|jor|lel|mat|med|mil|mus|net|nom|not|ntr|odo|org|ppg|pro|psc|psi|qsl|rec|slg|srv|tmp|trd|tur|tv|vet|zlg)\.br
|(?:com|net|org)\.bs
|(?:com|net|org)\.bz
|(?:ab|bc|mb|nb|nf|nl|ns|nt|nu|on|pe|qc|sk|yk|gc)\.ca
|(?:co|net|org|edu|gov)\.ck
|(?:com|edu|gov|net|org|ac|ah|bj|cq|gd|gs|gx|gz|hb|he|hi|hk|hl|hn|jl|js|ln|mo|nm|nx|qh|sc|sn|sh|sx|tj|tw|xj|xz|yn|zj)\.cn
|(?:arts|com|edu|firm|gov|info|int|nom|mil|org|rec|store|web)\.co
|(?:ac|co|ed|fi|go|or|sa)\.cr
|(?:com|net|org)\.cu
|(?:ac|com|gov|net|org)\.cy
|(?:co)\.dk
|(?:art|com|edu|gov|gob|org|mil|net|sld|web)\.do
|(?:com|org|net|gov|edu|ass|pol|art)\.dz
|(?:com|k12|edu|fin|med|gov|mil|org|net)\.ec
|(?:com|pri|fie|org|med)\.ee
|(?:com|edu|eun|gov|net|org|sci)\.eg
|(?:com|net|org|edu|mil|gov|ind)\.er
|(?:com|org|gob|edu|nom)\.es
|(?:com|gov|org|edu|net|biz|name|info)\.et
|(?:ac|com|gov|id|org|school)\.fj
|(?:com|ac|gov|net|nom|org)\.fk
|(?:asso|nom|barreau|com|prd|presse|tm|aeroport|assedic|avocat|avoues|cci|chambagri|chirurgiens-dentistes|experts-comptables|geometre-expert|gouv|greta|huissier-justice|medecin|notaires|pharmacien|port|veterinaire)\.fr
|(?:com|edu|gov|mil|net|org|pvt)\.ge
|(?:co|org|sch|ac|gov|ltd|ind|net|alderney|guernsey|sark)\.gg
|(?:com|edu|gov|net|org)\.gr
|(?:com|edu|net|gob|org|mil|ind)\.gt
|(?:com|edu|net|org|gov|mil)\.gu
|(?:com|net|org|idv|gov|edu)\.hk
|(?:co|2000|erotika|jogasz|sex|video|info|agrar|film|konyvelo|shop|org|bolt|forum|lakas|suli|priv|casino|games|media|szex|sport|city|hotel|news|tozsde|tm|erotica|ingatlan|reklam|utazas)\.hu
|(?:ac|co|go|mil|net|or)\.id
|(?:co|net|org|ac|gov|k12|muni|idf)\.il
|(?:co|net|org|ac|lkd\.co|gov|nic|plc\.co)\.im
|(?:co|net|ac|ernet|gov|nic|res|gen|firm|mil|org|ind)\.in
|(?:ac|co|gov|id|net|org|sch)\.ir
|(?:ac|co|net|org|gov|ind|jersey|ltd|sch)\.je
|(?:com|org|net|gov|edu|mil)\.jo
|(?:ad|ac|co|go|or|ne|gr|ed|lg|net|org|gov|hokkaido|aomori|iwate|miyagi|akita|yamagata|fukushima|ibaraki|tochigi|gunma|saitama|chiba|tokyo|kanagawa|niigata|toyama|ishikawa|fukui|yamanashi|nagano|gifu|shizuoka|aichi|mie|shiga|kyoto|osaka|hyogo|nara|wakayama|tottori|shimane|okayama|hiroshima|yamaguchi|tokushima|kagawa|ehime|kochi|fukuoka|saga|nagasaki|kumamoto|oita|miyazaki|kagoshima|okinawa|sapporo|sendai|yokohama|kawasaki|nagoya|kobe|kitakyushu|utsunomiya|kanazawa|takamatsu|matsuyama)\.jp
|(?:com|net|org|edu|gov|mil)\.kg
|(?:com|net|org|per|edu|gov|mil)\.kh
|(?:ac|co|go|ne|or|pe|re|seoul|kyonggi)\.kr
|(?:com|net|org|edu|gov)\.kw
|(?:com|net|org)\.la
|(?:com|org|net|edu|gov|mil)\.lb
|(?:com|edu|gov|net|org)\.lc
|(?:com|net|org|edu|gov|mil|id|asn|conf)\.lv
|(?:com|net|org)\.ly
|(?:co|net|org|press|ac)\.ma
|(?:com)\.mk
|(?:com|net|org|edu|gov)\.mm
|(?:com|org|edu|gov|museum)\.mn
|(?:com|net|org|edu|gov)\.mo
|(?:com|net|org|edu|tm|uu)\.mt
|(?:com|net|org|gob|edu)\.mx
|(?:com|org|gov|edu|net)\.my
|(?:com|org|net|alt|edu|cul|unam|telecom)\.na
|(?:com|net|org)\.nc
|(?:ac|edu|sch|com|gov|org|net)\.ng
|(?:gob|com|net|edu|nom|org)\.ni
|(?:com|net|org|gov|edu)\.np
|(?:ac|co|cri|gen|geek|govt|iwi|maori|mil|net|org|school)\.nz
|(?:com|co|edu|ac|gov|net|org|mod|museum|biz|pro|med)\.om
|(?:com|net|org|edu|ac|gob|sld)\.pa
|(?:edu|gob|nom|mil|org|com|net)\.pe
|(?:com|net|ac)\.pg
|(?:com|net|org|mil|ngo)\.ph
|(?:aid|agro|atm|auto|biz|com|edu|gmina|gsm|info|mail|miasta|media|mil|net|nieruchomosci|nom|org|pc|powiat|priv|realestate|rel|sex|shop|sklep|sos|szkola|targi|tm|tourism|travel|turystyka)\.pl
|(?:com|net|edu|org|fam|biz|web|gov|gob|gok|gon|gop|gos)\.pk
|(?:edu|gov|plo|sec)\.ps
|(?:com|edu|gov|int|net|nome|org|publ)\.pt
|(?:com|net|org|edu)\.py
|(?:com|net|org|edu|gov)\.qa
|(?:asso|com|nom)\.re
|(?:com|org|tm|nt|nom|info|rec|arts|firm|store|www)\.ro
|(?:ac|adygeya|altai|amur|amursk|arkhangelsk|astrakhan|baikal|bashkiria|belgorod|bir|bryansk|buryatia|cbg|chel|chelyabinsk|chita|chukotka|chuvashia|cmw|com|dagestan|dudinka|e-burg|edu|fareast|gov|grozny|int|irkutsk|ivanovo|izhevsk|jamal|jar|joshkar-ola|k-uralsk|kalmykia|kaluga|kamchatka|karelia|kazan|kchr|kemerovo|khabarovsk|khakassia|khv|kirov|kms|koenig|komi|kostroma|krasnoyarsk|kuban|kurgan|kursk|kustanai|kuzbass|lipetsk|magadan|magnitka|mari-el|mari|marine|mil|mordovia|mosreg|msk|murmansk|mytis|nakhodka|nalchik|net|nkz|nnov|norilsk|nov|novosibirsk|nsk|omsk|orenburg|org|oryol|oskol|palana|penza|perm|pp|pskov|ptz|pyatigorsk|rnd|rubtsovsk|ryazan|sakhalin|samara|saratov|simbirsk|smolensk|snz|spb|stavropol|stv|surgut|syzran|tambov|tatarstan|test|tom|tomsk|tsaritsyn|tsk|tula|tuva|tver|tyumen|udm|udmurtia|ulan-ude|vdonsk|vladikavkaz|vladimir|vladivostok|volgograd|vologda|voronezh|vrn|vyatka|yakutia|yamal|yaroslavl|yekaterinburg|yuzhno-sakhalinsk|zgrad)\.ru
|(?:com|edu|sch|med|gov|net|org|pub)\.sa
|(?:com|net|org|edu|gov)\.sb
|(?:com|net|org|edu|sch|med|gov)\.sd
|(?:tm|press|parti|brand|fh|fhsk|fhv|komforb|kommunalforbund|komvux|lanarb|lanbib|naturbruksgymn|sshn|org|pp)\.se
|(?:com|net|org|edu|gov|per)\.sg
|(?:com|net|org|edu|gov|mil)\.sh
|(?:gov|saotome|principe|consulado|embaixada|org|edu|net|com|store|mil|co)\.st
|(?:com|org|edu|gob|red)\.sv
|(?:com|net|org|gov)\.sy
|(?:ac|co|go|net|or)\.th
|(?:com|net|org|edunet|gov|ens|fin|nat|ind|info|intl|rnrt|rnu|rns|tourism)\.tn
|(?:com|net|org|edu|gov|mil|bbs|k12|gen)\.tr
|(?:co|com|org|net|biz|info|pro|int|coop|jobs|mobi|travel|museum|aero|name|gov|edu|nic|us|uk|ca|eu|es|fr|it|se|dk|be|de|at|au)\.tt
|(?:co)\.tv
|(?:com|net|org|edu|idv|gov)\.tw
|(?:com|gov|net|edu|org|in|cherkassy|ck|chernigov|cn|chernovtsy|cv|crimea|dnepropetrovsk|dp|donetsk|dn|ivano-frankivsk|if|kharkov|kh|kherson|ks|khmelnitskiy|km|kiev|kv|kirovograd|kr|lugansk|lg|lutsk|lviv|nikolaev|mk|odessa|od|poltava|pl|rovno|rv|sebastopol|sumy|ternopil|te|uzhgorod|vinnica|vn|zaporizhzhe|zp|zhitomir|zt)\.ua
|(?:ac|co|or|go)\.ug
|(?:co|me|org|edu|ltd|plc|net|sch|nic|ac|gov|nhs|police|mod)\.uk
|(?:dni|fed)\.us
|(?:com|edu|net|org|gub|mil)\.uy
|(?:com|net|org|co|edu|gov|mil|arts|bib|firm|info|int|nom|rec|store|tec|web)\.ve
|(?:co|net|org)\.vi
|(?:com|biz|edu|gov|net|org|int|ac|pro|info|health|name)\.vn
|(?:com|edu|net|org|de|ch|fr)\.vu
|(?:com|net|org|gov|edu)\.ws
|(?:ac|co|edu|org)\.yu
|(?:com|net|org|gov|edu|mil)\.ye
|(?:ac|alt|bourse|city|co|edu|gov|law|mil|net|ngo|nom|org|school|tm|web)\.za
|(?:co|ac|org|gov)\.zw
|(?:eu)\.org
|(?:au|br|cn|de)\.com
|(?:de)\.net
|(?:eu|gb)\.com
|(?:gb)\.net
|(?:hu|no|qc|ru|sa|se|uk)\.com
|(?:uk)\.net
|(?:us|uy|za)\.com
|(?:dk)\.org
|(?:tel)\.no
|(?:fax|mob|mobil|mobile|tel|tlf)\.nr
|(?:e164)\.arpa)$
|(?:surbl)\.org""", re.I | re.X)

surbl = Blacklist()

