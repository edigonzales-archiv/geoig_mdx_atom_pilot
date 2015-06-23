#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import uuid

#identifier, namespace, title, abstract, metadata_link, "type", modified, canton, data_responsibility, x_min, y_min, x_max, y_max

namespace = "http://www.geo.so.ch"
type = 100
canton = "so"
data_responsibility = "agi"
title = "Amtliche Vermessung - Gemeinde "
abstract = "Amtliche Vermessung der Gemeinde "
metadata_link = "http://www.geocat.ch/geonetwork/srv/ger/csw?service=CSW&amp;version=2.0.2&amp;request=GetRecordById&amp;elementSetName=full&amp;outputFormat=application/xml&amp;outputSchema=IsoRecord&amp;id=ab7a03e2-4bdd-4a49-bd92-4b0028bfcd51"
uri = "http://www.catais.org/geodaten/ch/so/agi/av/dm01avch24d/itf/"

sql = """SELECT ST_XMax(ST_Transform(ST_Union(geometrie), 4326)) as x_max,
       ST_YMax(ST_Transform(ST_Union(geometrie), 4326)) as y_max,
       ST_XMin(ST_Transform(ST_Union(geometrie), 4326)) as x_min,
       ST_YMin(ST_Transform(ST_Union(geometrie), 4326)) as y_min,
       bfsnr, "name"
FROM av_mopublic.hoheitsgrenzen__gemeindegrenze
GROUP BY bfsnr, "name";"""

con = None

try:
    con = psycopg2.connect(database='xanadu2', user='stefan', password='ziegler12') 
    cur = con.cursor()
    cur.execute(sql)          
    rows = cur.fetchall()

    for row in rows:
        insert = "INSERT INTO metadb (identifier, namespace, title, abstract, metadata_link, \"type\", modified, canton, data_responsibility, x_min, y_min, x_max, y_max) VALUES ('"
    
        x_min = row[2]
        y_min = row[3]
        x_max = row[0]
        y_max = row[1]
        bfsnr = row[4]
        gem_name = row[5]
        
        my_uuid = str(uuid.uuid4())
        
        insert += my_uuid + "', '" + namespace + "', "
        insert += "'" + title + gem_name + " (" + str(bfsnr) + ")', "
        insert += "'" + abstract + gem_name + " (" + str(bfsnr) + ")', "
        insert += "'" + metadata_link + "', " + str(type)  + ", '2015-04-01 06:00:00', '" + canton + "', '" + data_responsibility + "', "
        insert += str(x_min) + ", " + str(y_min) + ", " + str(x_max) + ", " + str(y_max) + ");"
        print insert
        
        insert = "INSERT INTO metadb_relation (metadb_id_parent, metadb_id_child) VALUES ('3d69c24a-3bc0-42fc-a4f1-3aef480fc5b9', '" + my_uuid + "');"
        print insert 
        
        insert = "INSERT INTO online_dataset (metadb_id, uri, format_mime, format_txt, srs_epsg, srs_txt, modified) VALUES ('"
        insert += my_uuid + "', '" + uri + "lv03/ch_" + str(bfsnr) + "00.itf', 'text/x-interlis1', 'INTERLIS1', 21781, 'CH1903/LV03', '2015-04-01 06:00:00');"
        print insert 
        

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
finally:
    if con:
        con.close()
        
    
