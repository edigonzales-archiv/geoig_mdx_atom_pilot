#!venv/bin/python
from flask import request
from flask import Flask
from flask import jsonify
from flask import json
from flask import Response
from logging.handlers import RotatingFileHandler 
from logging import Formatter
import logging

app = Flask(__name__)

@app.route('/ch/<canton>/dls/service.xml', methods=['GET'])
@app.route('/dls/service.xml', methods=['GET'])
def service_xml(canton='gl'):
    easting = request.args.get('easting', '')
    northing = request.args.get('northing', '')

    return "service.xml" + str(canton)

@app.route('/ch/<canton>/search/opensearchdescription.xml', methods=['GET'])
def search_opensearchdescription_xml(canton='gl'):
    return "search/opensearchdescription.xml"

@app.route('/ch/<canton>/dls', methods=['GET'])
def dls(canton='gl'):
    request_param = request.args.get('request', '')
    return request_param


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
