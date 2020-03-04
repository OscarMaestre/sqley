#!/bin/bash

rm ciclos.db
rm -rf gestionbd/migrations
rm -rf programaciones/migrations
rm -rf reparto/migrations
rm -rf tutoria/migrations
mkdir gestionbd/migrations/
mkdir programaciones/migrations/
mkdir reparto/migrations/
mkdir tutoria/migrations/
touch gestionbd/migrations/__init__.py
touch programaciones/migrations/__init__.py
touch reparto/migrations/__init__.py
touch tutoria/migrations/__init__.py
./manage.py makemigrations
./manage.py migrate

./dodo.py
./cargar_datos_iniciales.py
