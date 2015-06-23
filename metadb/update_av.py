#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import glob
import os.path 
import time
import datetime
import sqlite3 as lite

PATH = "/opt/Geodaten/ch/so/kva/av/dm01avch24d/itf/lv03/"
URL = "http://www.catais.org/geodaten/ch/so/agi/av/dm01avch24d/itf/lv03/"

SQLITE = "/home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite"

itf_list = glob.glob(PATH + "*.itf")

con = lite.connect(SQLITE)
with con:

    cur = con.cursor()    

    for itf in itf_list:
        print itf
        
        uri = URL + itf.split("/")[-1]
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(itf)).strftime("%Y-%m-%d %H:%M:%S")
        
        cur.execute("UPDATE online_dataset SET modified=? WHERE uri=?", (modified, uri))
        con.commit()
        print "Number of rows updated: %d" % cur.rowcount
        
        cur.execute("SELECT metadb_id FROM online_dataset WHERE uri='" + uri + "'")
        
        while True:
            row = cur.fetchone()
        
            if row == None:
                break        
                
            metadb_id = str(row[0])
            cur.execute("UPDATE metadb SET modified=? WHERE identifier=?", (modified, metadb_id))
            con.commit()
            print "Number of rows updated: %d" % cur.rowcount
