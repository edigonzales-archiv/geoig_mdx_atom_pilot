#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import glob
import os.path 
import time
import datetime
import sqlite3 as lite

PATH_ITF_CH_LV03 = "/opt/Geodaten/ch/so/kva/av/dm01avch24d/itf/lv03/"
PATH_ITF_CH_LV95 = "/opt/Geodaten/ch/so/kva/av/dm01avch24d/itf/lv95/"
PATH_DXF_GEOBAU_LV03 = "/opt/Geodaten/ch/so/kva/av/geobau/dxf/"
PATH_GPKG_LV03 = "/opt/Geodaten/ch/so/kva/av/mopublic/gpkg/lv03/d/"

URL_ITF_CH_LV03 = "http://www.catais.org/geodaten/ch/so/agi/av/dm01avch24d/itf/lv03/"
URL_ITF_CH_LV95 = "http://www.catais.org/geodaten/ch/so/agi/av/dm01avch24d/itf/lv95/"
URL_DXF_GEOBAU_LV03 = "http://www.catais.org/geodaten/ch/so/agi/av/geobau/dxf/"
URL_GPKG_LV03 = "http://www.catais.org/geodaten/ch/so/agi/av/mopublic/gpkg/lv03/d/"

SQLITE = "/home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite"


con = lite.connect(SQLITE)
with con:

    cur = con.cursor()    

    # ITF-CH / LV03
    itf_list = glob.glob(PATH_ITF_CH_LV03 + "*.itf")
    for itf in itf_list:
        print itf
        
        uri = URL_ITF_CH_LV03 + itf.split("/")[-1]
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

    # ITF-CH / LV95
    itf_list = glob.glob(PATH_ITF_CH_LV95 + "*.itf")
    for itf in itf_list:
        print itf
        
        uri = URL_ITF_CH_LV95 + itf.split("/")[-1]
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


    # DXF-GEOBAU / LV03
    dxf_list = glob.glob(PATH_DXF_GEOBAU_LV03 + "*.dxf")
    for dxf in dxf_list:
        print dxf
        
        uri = URL_DXF_GEOBAU_LV03 + dxf.split("/")[-1]
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(dxf)).strftime("%Y-%m-%d %H:%M:%S")
        
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

    # GPKG / LV03
    gpkg_list = glob.glob(PATH_GPKG_LV03 + "*.gpkg")
    for gpkg in gpkg_list:
        print gpkg
        
        uri = URL_GPKG_LV03 + gpkg.split("/")[-1]
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(gpkg)).strftime("%Y-%m-%d %H:%M:%S")
        
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
