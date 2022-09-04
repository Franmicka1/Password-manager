#!/bin/bash

python3 tajnik.py init mAsterPasswrd
python3 tajnik.py put mAsterPasswrd www.fer.hr neprobojAsifrA
python3 tajnik.py get mAsterPasswrd www.fer.hr
python3 tajnik.py get wrongPasswrd www.fer.hr

echo

python3 tajnik.py init master
python3 tajnik.py put master2 nova sifra
python3 tajnik.py get master2 nova
python3 tajnik.py put master nova
python3 tajnik.py get master
python3 tajnik.py put master nova sifra
python3 tajnik.py get master nova
python3 tajnik.py put master nova sifra2
python3 tajnik.py get master nova
python3 tajnik.py get master nova2







