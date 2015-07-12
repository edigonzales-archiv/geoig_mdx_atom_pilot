#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import glob
import os.path 
import time
import datetime
import sqlite3 as lite

SQLITE = "/home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite"

con = lite.connect(SQLITE)
with con:

    cur = con.cursor()    
    cur.execute("DROP TABLE fts_metadb;")
    cur.execute("CREATE VIRTUAL TABLE fts_metadb USING fts3(id INTEGER PRIMARY KEY, m_pkuid, identifier, namespace, title, abstract, canton, data_responsibility, d_pkuid, uri, format_mime, format_txt, srs_epsg, srs_txt, modified);");
    cur.execute("INSERT INTO fts_metadb(id, m_pkuid, identifier, namespace, title, abstract, canton, data_responsibility, d_pkuid, uri, format_mime, format_txt, srs_epsg, srs_txt, modified) SELECT d.rowid, m.pkuid as m_pkuid, m.identifier, m.namespace, m.title, m.abstract, m.canton, m.data_responsibility, d.pkuid as d_pkuid, d.uri, d.format_mime, d.format_txt, d.srs_epsg, d.srs_txt, d.modified FROM metadb m, online_dataset d WHERE m.identifier = d.metadb_id AND m.type = 100;")    
    con.commit()
    print "Number of rows updated: %d" % cur.rowcount
        
