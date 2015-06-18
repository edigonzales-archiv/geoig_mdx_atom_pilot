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
from sqlalchemy.sql.expression import cast
import sqlalchemy
from logging.handlers import RotatingFileHandler 
from logging import Formatter
import logging
import datetime
from pytz import timezone

# DON'T FORGET TO LOG!!!!!!

app = Flask(__name__)

# We want to use existing tables from the sqlite database.
Base = automap_base()
#engine = create_engine("sqlite://///home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite")
engine = create_engine("sqlite://///home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite", encoding='utf8', convert_unicode=True)
Base.prepare(engine, reflect=True)

MetaDb = Base.classes.metadb
OnlineDataset = Base.classes.online_dataset
session = Session(engine)

@app.route('/dls/service.xml', methods=['GET'])
def service_feed_xml():    
    # For correct rendering of the datetime we need a timezone.
    # Really not sure about this whole timezone stuff:
    # - May I use %z?
    # - Is the comparison correct?
    my_timezone = timezone('Europe/Amsterdam')    
    
    # We need to know the date/time of the last modification of *any* data.
    max_modified = datetime.datetime.strptime( "1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S" )
 
    # list for template
    items = []
 
    # If you only want all the rows w/o frills you hast have to use .query(MetaDb).
    # You could also do the bounding box thing here in the application.
    for row in session.query(MetaDb.identifier, MetaDb.namespace, MetaDb.title, MetaDb.abstract, MetaDb.metadata_link, MetaDb.modified, MetaDb.canton, \
        (cast(MetaDb.y_min, sqlalchemy.String) + " " + cast(MetaDb.x_min, sqlalchemy.String) + " " + \
        cast(MetaDb.y_max, sqlalchemy.String)  + " " + cast(MetaDb.x_max, sqlalchemy.String)).label("bbox")).filter(MetaDb.type==100):
        
        item = {}
        item['identifier'] = row.identifier
        item['namespace'] = row.namespace
        item['title'] = row.title
        item['abstract'] = row.abstract
        item['metadata_link'] = row.metadata_link
        item['modified'] = my_timezone.localize(row.modified).strftime('%Y-%m-%dT%H:%M:%S%z')        
        item['canton'] = row.canton
        item['bbox'] = row.bbox
        
        if row.modified > max_modified:
            max_modified = row.modified
        
        items.append(item)
                
    max_modified = my_timezone.localize(max_modified).strftime('%Y-%m-%dT%H:%M:%S%z')
    print max_modified
        
    return render_template('servicefeed.xml', items = items, max_modified = max_modified)

@app.route('/search/opensearchdescription.xml', methods=['GET'])
def search_opensearchdescription_xml():
    return "search/opensearchdescription.xml"

@app.route('/dls/<metadb_id>', methods=['GET'])
def dataset_feed_xml(metadb_id):
    metadb_id = metadb_id.split(".")[0]
    
    # see above
    items = []
    my_timezone = timezone('Europe/Amsterdam')    
    max_modified = datetime.datetime.strptime( "1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S" )

    
    for row in session.query(OnlineDataset.metadb_id, OnlineDataset.uri, OnlineDataset.format_mime, \
        OnlineDataset.format_txt, OnlineDataset.srs_epsg, OnlineDataset.srs_txt, OnlineDataset.modified, (MetaDb.title +
        " - Bezugssystem " + OnlineDataset.srs_txt + " - Format " + OnlineDataset.format_txt).label("dataset_title")).join(MetaDb, OnlineDataset.metadb_id==MetaDb.identifier).filter(OnlineDataset.metadb_id==metadb_id).order_by(OnlineDataset.uri):    
        
        print row.dataset_title
        #
        item = {}
        item['identifier'] = row.identifier
        item['namespace'] = row.namespace
        item['title'] = row.title
        item['abstract'] = row.abstract
        item['metadata_link'] = row.metadata_link
        item['modified'] = my_timezone.localize(row.modified).strftime('%Y-%m-%dT%H:%M:%S%z')        
        item['canton'] = row.canton
        item['bbox'] = row.bbox
        
        if row.modified > max_modified:
            max_modified = row.modified
        
        items.append(item)
        
    return metadb_id




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
