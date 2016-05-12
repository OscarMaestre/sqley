#!/usr/bin/env python3
# coding=utf-8
import yaml, sys

ciclo=open ( sys.argv[1] )

y=yaml.load(ciclo)
print (yaml.dump(y))
ciclo.close()