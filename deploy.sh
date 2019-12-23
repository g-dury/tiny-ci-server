#!/bin/bash

cd /var/www/dury.pro/html/
git pull
COMMIT=`git rev-parse --short HEAD`
message="<html><body><h3> DURY.PRO Website Update: Done </h3><br><p>Live commit: $COMMIT</p><br><p>Cheers</p></body></html>"
mail -s 'Dury.pro website update OK' -a 'Content-Type: text/html' -a From:Admin\<admin@dury.pro\> gdury69@gmail.com <<< $message
