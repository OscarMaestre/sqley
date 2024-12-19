#!/usr/bin/env python3


import os
import telegram
archivo=os.environ["TR_TORRENT_NAME"]


telegram.send("Se ha completado el torrent " + archivo)