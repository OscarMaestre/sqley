#!/bin/bash

rm ciclos.db
./manage.py makemigrations
./manage.py migrate
./dodo.py
./cargar_datos_iniciales.py
