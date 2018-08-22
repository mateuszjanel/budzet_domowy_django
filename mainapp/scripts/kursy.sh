#!/bin/bash
. /opt/glownyproject/env/bin/activate
rm dane
curl -X GET http://api.nbp.pl/api/exchangerates/tables/{A}/?format=json | python -m json.tool >> dane
python /opt/glownyproject/aplikacja/manage.py runscript currency
python /opt/glownyproject/aplikacja/manage.py runscript transakcjestale
deactivate
