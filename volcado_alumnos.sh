#!/bin/bash

DB=ciclos.db
RESULTADO=alumnos.sql

#INICIO: se crear el archivo RESULTADO
sqlite3 $DB '.dump ciclos'       >  $RESULTADO

#El resto de datos se añaden a continuación
sqlite3 $DB '.dump cursos'       >> $RESULTADO
sqlite3 $DB '.dump modulos'      >> $RESULTADO
sqlite3 $DB '.dump alumnos'      >> $RESULTADO
sqlite3 $DB '.dump matriculas'   >> $RESULTADO
