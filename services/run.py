#!venv/bin/python
from flask import request
from flask import Flask
from flask import jsonify
from flask import json
from flask import Response
from logging.handlers import RotatingFileHandler 
from logging import Formatter
import logging



#DTM_VRT = "/home/stefan/Downloads/dtm/grid/50cm/dtm.vrt"
#DSM_VRT = "/home/stefan/Downloads/dom/grid/50cm/dom.vrt"

#DTM_VRT = "/opt/Geodaten/ch/so/kva/hoehen/2014/dtm/grid/50cm/dtm.vrt"
#DSM_VRT = "/opt/Geodaten/ch/so/kva/hoehen/2014/dom/grid/50cm/dom.vrt"

DTM_VRT = "/home/stefan/Projekte/api_rest_hoehen/dtm.vrt"
DSM_VRT = "/home/stefan/Projekte/api_rest_hoehen/dom.vrt"

# File path of chenyx06a.gsb hardcoded!
S_SRS = "+proj=somerc +lat_0=46.952405555555555N +lon_0=7.439583333333333E +ellps=bessel +x_0=2600000 +y_0=1200000 +towgs84=674.374,15.056,405.346 +units=m +k_0=1 +nadgrids=@null"
T_SRS = "+proj=somerc +lat_0=46.952405555555555N +lon_0=7.439583333333333E +ellps=bessel +x_0=600000 +y_0=200000 +towgs84=674.374,15.056,405.346 +units=m +units=m +k_0=1 +nadgrids=/home/stefan/Projekte/api_rest_hoehen/chenyx06a.gsb"

app = Flask(__name__)

@app.route('/service.xml', methods=['GET'])
def service_xml():
    easting = request.args.get('easting', '')
    northing = request.args.get('northing', '')

    return "service.xml"

@app.route('/search/opensearchdescription.xml', methods=['GET'])
def search_opensearchdescription_xml():
    return "search/opensearchdescription.xml"

@app.route('/search', methods=['GET'])
def search():
    request_param = request.args.get('request', '')
    return request_param


if __name__ == '__main__':
    app.run(debug=True)

#http://127.0.0.1:5000/search?request=GetDownloadServiceMetadata

#http://geodaten.llv.li/atom/service.xml

#http://geodaten.llv.li/atom/search/opensearchdescription.xml
#http://geodaten.llv.li/atom/search/search.php?request=GetDownloadServiceMetadata
#http://geodaten.llv.li/atom/search/search.php?request=describespatialdataset&spatial_dataset_identifier_code=tba_denkmalschutzobjekte

#http://geodaten.llv.li/atom/search/search.php?request=GetSpatialDataset&spatial_dataset_identifier_code=tba_denkmalschutzobjekte&language=de&crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F2056&mediatype=text%2Fxml%3Bsubtype%3Dgml%2F3.1.1
#http://geodaten.llv.li/atom/search/search.php?request=GetSpatialDataset&spatial_dataset_identifier_code=tba_denkmalschutzobjekte&language=de&crs=http://www.opengis.net/def/crs/EPSG/0/2056&mediatype=text/xml;subtype=gml/3.1.1

#http://geodaten.llv.li/atom/search/search.php?q=test   
