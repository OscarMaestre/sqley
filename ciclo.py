#!/usr/bin/env python3
# coding=utf-8
import yaml, sys

ciclo=open ( sys.argv[1], encoding="utf-8" )

y=yaml.safe_load(ciclo)
#print (yaml.dump(y))
for k in y.keys():
    print (k)
print (y["ciclo"]["modulos"][1])
ciclo.close()