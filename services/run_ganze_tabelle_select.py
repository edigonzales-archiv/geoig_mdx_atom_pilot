#!venv/bin/python
from flask import request
from flask import Flask
from flask import jsonify
from flask import json
from flask import Response
from flask import render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from logging.handlers import RotatingFileHandler 
from logging import Formatter
import logging
#import jinja2

app = Flask(__name__)

# We want to use existing tables in the sqlite database.
Base = automap_base()
#engine = create_engine("sqlite://///home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite", encoding='utf8', convert_unicode=True)
engine = create_engine("sqlite://///home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite", encoding='utf8', convert_unicode=True)
Base.prepare(engine, reflect=True)

MetaDb = Base.classes.metadb
session = Session(engine)

@app.route('/dls/service.xml', methods=['GET'])
def service_xml():
    easting = request.args.get('easting', '')
    northing = request.args.get('northing', '')

    items = []
    #entries = [dict(title=row[0], text=row[1]) for row in session.query(MetaDb).filter(MetaDb.type==100)] 
    #print entries
        #print row.identifier, row.title
        #print row
         
        #items.append(row)
        
    #for row in session.query(MetaDb.filter(MetaDb.type==100):
    for row in session.query(MetaDb.identifier, MetaDb.title).filter(MetaDb.type==100):
        print row
        #print row2dict(row)
        #items.append(row2dict(row))
        
    #return render_template('servicefeed.xml', items = items)
    return "service.xml"

@app.route('/search/opensearchdescription.xml', methods=['GET'])
def search_opensearchdescription_xml():
    return "search/opensearchdescription.xml"

@app.route('/dls', methods=['GET'])
def dls():
    request_param = request.args.get('request', '')
    return request_param


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = unicode(getattr(row, column.name))
    return d

if __name__ == '__main__':
    app.run(debug=True)

#http://127.0.0.1:5000/ch/gl/search/opensearchdescription.xml
#http://127.0.0.1:5000/ch/gl/dls?request=GetDownloadServiceMetadata
#http://127.0.0.1:5000/ch/gl/dls/service.xml

#http://geodaten.llv.li/atom/service.xml

#http://geodaten.llv.li/atom/search/opensearchdescription.xml
#http://geodaten.llv.li/atom/search/search.php?request=GetDownloadServiceMetadata
#http://geodaten.llv.li/atom/search/search.php?request=describespatialdataset&spatial_dataset_identifier_code=tba_denkmalschutzobjekte

#http://geodaten.llv.li/atom/search/search.php?request=GetSpatialDataset&spatial_dataset_identifier_code=tba_denkmalschutzobjekte&language=de&crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F2056&mediatype=text%2Fxml%3Bsubtype%3Dgml%2F3.1.1
#http://geodaten.llv.li/atom/search/search.php?request=GetSpatialDataset&spatial_dataset_identifier_code=tba_denkmalschutzobjekte&language=de&crs=http://www.opengis.net/def/crs/EPSG/0/2056&mediatype=text/xml;subtype=gml/3.1.1

#http://geodaten.llv.li/atom/search/search.php?q=test   
