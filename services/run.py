#!venv/bin/python
from flask import request
from flask import Flask
from flask import jsonify
from flask import json
from flask import Response
from flask import render_template
from flask import make_response
from flask import abort
from flask import redirect
from sqlalchemy.dialects import sqlite
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.sql.expression import cast
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
import sqlalchemy
from logging.handlers import RotatingFileHandler 
from logging import Formatter
import logging
import datetime
import urllib
from pytz import timezone

SERVICE_URL = "http://www.catais.org/geoig/services/dls"
SEARCH_URL = "http://www.catais.org/geoig/services/search"
#SERVICE_URL = "http://127.0.0.1:5000/dls"
#SEARCH_URL = "http://127.0.0.1:5000/search"


# http://flask-restful.readthedocs.org/en/latest/reqparse.html

app = Flask(__name__)

# We want to use existing tables from the sqlite database.
Base = automap_base()
engine = create_engine("sqlite://///home/stefan/Projekte/geoig_mdx_atom_pilot/metadb/metadb.sqlite", encoding='utf8', convert_unicode=True)
Base.prepare(engine, reflect=True)

MetaDb = Base.classes.metadb
OnlineDataset = Base.classes.online_dataset
session = Session(engine)

# Sqlite virtual table ist not automapped.
# Not sure why. Missing Pk? But I did add one.
m = MetaData()
m.reflect(engine)
FtsMetaDb = Table('fts_metadb', m)

@app.route('/dls/ch/<canton>/<data_responsibility>/service.xml', methods=['GET'])
@app.route('/dls/ch/<canton>/service.xml', methods=['GET'])
@app.route('/dls/ch/service.xml', methods=['GET'])
@app.route('/dls/service.xml', methods=['GET'])
def service_feed_xml(canton='', data_responsibility=''): 
    app.logger.debug('service feed request')
       
    # If there is no canton and/or data_responsiblity we
    # need to initialize the service_url.
    service_url = SERVICE_URL
    search_url = SEARCH_URL

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
    query = session.query(MetaDb.identifier, MetaDb.namespace, MetaDb.title, MetaDb.abstract, MetaDb.metadata_link, MetaDb.modified, MetaDb.canton, \
        (cast(MetaDb.y_min, sqlalchemy.String) + " " + cast(MetaDb.x_min, sqlalchemy.String) + " " + \
        cast(MetaDb.y_max, sqlalchemy.String)  + " " + cast(MetaDb.x_max, sqlalchemy.String)).label("bbox")). \
        filter(MetaDb.type==100)    

    if canton:
        query = query.filter(MetaDb.canton==canton)
        service_url = SERVICE_URL + "/ch/" + canton
        search_url = SEARCH_URL + "/ch/" + canton
        
    if data_responsibility:
        query = query.filter(MetaDb.data_responsibility==data_responsibility)   
        service_url += "/" + data_responsibility
        search_url += "/" + data_responsibility
    
    app.logger.debug('SQL: %s', str(query.statement.compile(dialect=sqlite.dialect())))
         
    for row in query:
        item = {}
        item['identifier'] = row.identifier
        item['namespace'] = row.namespace
        item['title'] = row.title
        item['abstract'] = row.abstract
        item['metadata_link'] = row.metadata_link
        item['modified'] = my_timezone.localize(row.modified).isoformat('T')
        item['canton'] = row.canton
        item['bbox'] = row.bbox
        
        if row.modified > max_modified:
            max_modified = row.modified
            max_modified_formated = my_timezone.localize(row.modified).isoformat('T')            
        
        app.logger.debug("modified: " + item['modified'])
        
        items.append(item)
    
    # This is for the header of the template (outside the for loop).
    max_modified = my_timezone.localize(max_modified).isoformat('T')
    
    app.logger.debug('service_url: %s', service_url)

    response = make_response(render_template('servicefeed.xml', items = items, max_modified_formated = max_modified, service_url = service_url, search_url = search_url))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response    

@app.route('/dls/ch/<canton>/<data_responsibility>/<metadb_id>', methods=['GET'])
@app.route('/dls/ch/<canton>/<metadb_id>', methods=['GET'])
@app.route('/dls/ch/<metadb_id>', methods=['GET'])
@app.route('/dls/<metadb_id>', methods=['GET'])
def dataset_feed_xml(metadb_id, canton='', data_responsibility=''):
    app.logger.debug('dataset feed request')
    
    metadb_id = metadb_id.split(".")[0]
    app.logger.debug('metadb_id: %s', str(metadb_id))
        
    # See comments in service feed method.
    items = []
    my_timezone = timezone('Europe/Amsterdam')    
    max_modified = datetime.datetime.strptime( "1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S" )

    query = session.query(OnlineDataset.metadb_id, OnlineDataset.uri, OnlineDataset.format_mime, \
        OnlineDataset.format_txt, OnlineDataset.srs_epsg, OnlineDataset.srs_txt, OnlineDataset.modified, MetaDb.title, \
        MetaDb.abstract, (MetaDb.title + \
        " - Bezugssystem " + OnlineDataset.srs_txt + " - Format " + OnlineDataset.format_txt).label("dataset_title"), \
        (cast(MetaDb.y_min, sqlalchemy.String) + " " + cast(MetaDb.x_min, sqlalchemy.String) + " " + \
        cast(MetaDb.y_max, sqlalchemy.String)  + " " + cast(MetaDb.x_max, sqlalchemy.String)).label("bbox")) \
        .join(MetaDb, OnlineDataset.metadb_id==MetaDb.identifier) \
        .filter(OnlineDataset.metadb_id==metadb_id).order_by(OnlineDataset.uri)
        
    app.logger.debug('SQL: %s', str(query.statement.compile(dialect=sqlite.dialect())))

    for row in query:    
        item = {}
        item['metadb_id'] = row.metadb_id
        item['uri'] = row.uri
        item['format_mime'] = row.format_mime
        item['format_txt'] = row.format_txt
        item['srs_epsg'] = row.srs_epsg
        item['srs_txt'] = row.srs_txt
        item['modified'] = my_timezone.localize(row.modified).isoformat('T')
        item['title'] = row.title
        item['abstract'] = row.abstract
        item['dataset_title'] = row.dataset_title
        item['bbox'] = row.bbox
        
        if row.modified > max_modified:
            max_modified = row.modified
            max_modified_formated = my_timezone.localize(row.modified).isoformat('T')
        
        items.append(item)
    
    service_url = SERVICE_URL
    if canton:
        service_url = SERVICE_URL + "/ch/" + canton
        
    if data_responsibility:
        service_url += "/" + data_responsibility
    
    # These are some variables we use in the header of the template (outside the for loop).
    if len(items):
        title = items[0]['title']
        identifier = items[0]['metadb_id']
        
    app.logger.debug('service_url: %s', service_url)

    response = make_response(render_template('datasetfeed.xml', items = items, service_url = service_url, max_modified = max_modified_formated, title = title, identifier = identifier))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response    

@app.route('/search/ch/<canton>/<data_responsibility>/opensearchdescription.xml', methods=['GET'])
@app.route('/search/ch/<canton>/opensearchdescription.xml', methods=['GET'])
@app.route('/search/ch/opensearchdescription.xml', methods=['GET'])
@app.route('/search/opensearchdescription.xml', methods=['GET'])
def opensearchdescription_xml(canton='', data_responsibility=''):
    # Create the correct url depending on the request.
    search_url = SEARCH_URL

    if canton:
        search_url = SEARCH_URL + "/ch/" + canton

    if data_responsibility:
        search_url += "/" + data_responsibility

    app.logger.debug('search_url: %s', search_url)

    # Get all possible formats (mime types).
    # NEEDS TO BE TESTED!!!
    query = session.query(OnlineDataset.format_mime) \
        .join(MetaDb, OnlineDataset.metadb_id==MetaDb.identifier) 
        
    if canton:
        query = query.filter(MetaDb.canton==canton)
        
    if data_responsibility:
        query = query.filter(MetaDb.data_responsibility==data_responsibility)   

    mime_types = []
    for row in query.distinct().order_by(OnlineDataset.format_mime):
        mime_types.append(row.format_mime)
        
    # Get 'example' datasets. We assume (=hardcoded) that epsg:21781 is the default crs 
    # (and always available).
    # Get only one dataset -> 'distinct on'
    #query = session.query(OnlineDataset.metadb_id, OnlineDataset.metadb_id, MetaDb.namespace, MetaDb.title, MetaDb.canton) \
    query = session.query(func.max(OnlineDataset.metadb_id), OnlineDataset.metadb_id, MetaDb.namespace, MetaDb.title) \
    .join(MetaDb, OnlineDataset.metadb_id==MetaDb.identifier)

    # Show raw sql query with correct dialect.
    #print str(query.statement.compile(dialect=sqlite.dialect()))

    if canton:
        query = query.filter(MetaDb.canton==canton)
    
    if data_responsibility:
        query = query.filter(MetaDb.data_responsibility==data_responsibility)

    app.logger.debug('SQL: %s', str(query.statement.compile(dialect=sqlite.dialect())))

    query = query.group_by(OnlineDataset.metadb_id).all()

    items = []
    for row in query:
        item = {}
        item['identifier'] = row.metadb_id
        item['namespace'] = row.namespace
        item['title'] = row.title
        items.append(item)
        
    response = make_response(render_template('opensearchdescription.xml', search_url = search_url, mime_types = mime_types, items = items))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response    

@app.route('/search/ch/<canton>/<data_responsibility>', methods=['GET'])
@app.route('/search/ch/<canton>', methods=['GET'])
@app.route('/search/ch', methods=['GET'])
@app.route('/search', methods=['GET'])
def search(canton='', data_responsibility=''):    
    params_len = len(request.args)
    
    if params_len == 0:
        abort(404)
    
    # Do the full text search only if 'q' is the only request parameter.
    query_param = request.args.get('q', '')
        
    if params_len == 1 and query_param:
        # Add some prefixes/wildcards. Not really sure how usefull this is.
        # I really do not understand this FTS.
        q = query_param.replace(' ', '*') + '*'
        
        # Find all datasets that match the search criteria.
        query = session.query(FtsMetaDb) 
        
        if canton:
            query = query.filter(FtsMetaDb.canton==canton)
        
        if data_responsibility:
            query = query.filter(FtsMetaDb.data_responsibility==data_responsibility)   
            
        query = query.filter("fts_metadb MATCH '"+q+"'")
        
        items = []
        for row in query:
            print row
            item = {}
            item['identifier'] = row.identifier
            item['namespace'] = row.namespace
            item['title'] = row.title
            item['abstract'] = row.abstract
            item['modified'] = row.modified
            item['format_mime'] = urllib.quote(row.format_mime)
            item['format_txt'] = row.format_txt
            item['srs_epsg'] = urllib.quote("http://www.opengis.net/def/crs/EPSG/0/" + str(row.srs_epsg))
            item['srs_txt'] = row.srs_txt
            item['uri'] = row.uri
            items.append(item)
            
            print urllib.quote(row.format_mime)

        response = make_response(render_template('results.html', items = items))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response    

    # Now we turn into 'service mode' and try to fulfill the requests.
    request_param = request.args.get('request', '')

    if request_param == "GetDownloadServiceMetadata":
        app.logger.debug('GetDownloadServiceMetadata')
        return service_feed_xml(canton, data_responsibility)
        
    elif request_param == "DescribeSpatialDataSet":
        app.logger.debug('DescribeSpatialDataSet')        
        identifier_code = request.args.get('spatial_dataset_identifier_code', '')
        identifier_namespace = request.args.get('spatial_dataset_identifier_namespace', '')
        type = request.args.get('type', '')
        crs = request.args.get('crs', '')
        # language is ignored
        # q is ignored
        
        if not identifier_code:
            abort(404)
        if not identifier_namespace:
            abort(404)
        if not type:
            abort(404)
        if not crs:
            abort(404)
        
        # We just need the pure epsg number.
        epsg = crs.split("/")[-1]
                    
        # Find dataset in meta database.
        try:
            dataset = session.query(OnlineDataset.metadb_id) \
                .join(MetaDb, OnlineDataset.metadb_id==MetaDb.identifier) \
                .filter(OnlineDataset.metadb_id==identifier_code) \
                .filter(MetaDb.namespace==identifier_namespace) \
                .filter(OnlineDataset.format_mime==type) \
                .filter(OnlineDataset.srs_epsg==epsg).one()
                
        # What is the response for these exceptions?
        except MultipleResultsFound, e:
            print e
            abort(404)
        except NoResultFound, e:
            print e
            abort(404)
    
        return dataset_feed_xml(dataset.metadb_id, canton, data_responsibility)
        
    elif request_param == "GetSpatialDataSet":
        app.logger.debug('GetSpatialDataSet')                
        identifier_code = request.args.get('spatial_dataset_identifier_code', '')
        identifier_namespace = request.args.get('spatial_dataset_identifier_namespace', '')
        type = request.args.get('type', '')
        crs = request.args.get('crs', '')
        # language is ignored
        # q is ignored
        
        if not identifier_code:
            abort(404)
        if not identifier_namespace:
            abort(404)
        if not type:
            abort(404)
        if not crs:
            abort(404)

        # We just need the pure epsg number.
        epsg = crs.split("/")[-1]
                    
        # Find dataset in meta database.
        try:
            dataset = session.query(OnlineDataset.uri) \
                .join(MetaDb, OnlineDataset.metadb_id==MetaDb.identifier) \
                .filter(OnlineDataset.metadb_id==identifier_code) \
                .filter(MetaDb.namespace==identifier_namespace) \
                .filter(OnlineDataset.format_mime==type) \
                .filter(OnlineDataset.srs_epsg==epsg).one()
                
        # What is the response for these exceptions?
        except MultipleResultsFound, e:
            app.logger.warning(str(e))                
            abort(404)
        except NoResultFound, e:
            app.logger.warning(str(e))                
            abort(404)
            
        if dataset.uri:
            return redirect(dataset.uri)
    else:
        abort(404)

if __name__ == '__main__':
    handler = RotatingFileHandler('atomfeed_opensearch.log', maxBytes=1048576, backupCount=3)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)    
    app.run(debug=True)
