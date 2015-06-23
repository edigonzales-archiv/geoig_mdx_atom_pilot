INSERT INTO "type" (code, code_txt) VALUES (0, 'undefined');
INSERT INTO "type" (code, code_txt) VALUES (1, 'root');
INSERT INTO "type" (code, code_txt) VALUES (100, 'dataset');
INSERT INTO "type" (code, code_txt) VALUES (200, 'wms');
INSERT INTO "type" (code, code_txt) VALUES (210, 'wmts');
INSERT INTO "type" (code, code_txt) VALUES (220, 'wfs');
INSERT INTO "type" (code, code_txt) VALUES (230, 'wcs');
INSERT INTO "type" (code, code_txt) VALUES (500, 'postgres');

-- Kanton Glarus / Stromversorgungssicherheit

INSERT INTO metadb (identifier, title, abstract, "type", canton, data_responsibility) VALUES ('ea5c61e7-1be8-4c3f-b7aa-4aa4f35072db', 'Stromversorgungssicherheit: Netzgebiete', 'Versorgungsgebiete im Starkstrombereich der Netzebenen (3,) 5, 7 mit Informationen über den Netzeigentümer sowie den Netzbetreiber.', 1, 'gl', 'efs');
INSERT INTO metadb (identifier, namespace, title, abstract, metadata_link, "type", modified, canton, data_responsibility, x_min, y_min, x_max, y_max) VALUES ('9565af3d-9d96-44bb-a9f8-de8e405c56f3', 'http://www.geo.gl.ch', 'Stromversorgungssicherheit: Netzgebiete', 'Versorgungsgebiete im Starkstrombereich der Netzebenen (3,) 5, 7 mit Informationen über den Netzeigentümer sowie den Netzbetreiber.', 'http://www.geocat.ch/geonetwork/srv/ger/csw?service=CSW&amp;version=2.0.2&amp;request=GetRecordById&amp;elementSetName=full&amp;outputFormat=application/xml&amp;outputSchema=IsoRecord&amp;id=88c57464-3a56-41c1-b8d4-45b019b62ce2', 100, '2015-04-01 06:00:00', 'gl', 'efs', 8.87124, 46.7965, 9.25259, 47.174);

INSERT INTO metadb_relation (metadb_id_parent, metadb_id_child) VALUES ('ea5c61e7-1be8-4c3f-b7aa-4aa4f35072db', '9565af3d-9d96-44bb-a9f8-de8e405c56f3');

INSERT INTO online_dataset (metadb_id, uri, format_mime, format_txt, srs_epsg, srs_txt, modified) VALUES ('9565af3d-9d96-44bb-a9f8-de8e405c56f3', 'http://www.catais.org/geodaten/ch/gl/efs/supplysecurity/xtf/lv03/supplysecurity.xtf', 'text/x-interlis23', 'INTERLIS23', '21781', 'CH1903/LV03', '2015-04-01 06:00:00');
INSERT INTO online_dataset (metadb_id, uri, format_mime, format_txt, srs_epsg, srs_txt, modified) VALUES ('9565af3d-9d96-44bb-a9f8-de8e405c56f3', 'http://www.catais.org/geodaten/ch/gl/efs/supplysecurity/gml/lv03/supplysecurity.gml', 'application/gml+xml;version=3.2', 'GML 3.2.1', '21781', 'CH1903/LV03', '2015-04-01 06:00:00');

<div style="float:left;"><img height="200" src="http://mdi.niedersachsen.de/preview_browser_metadata/Schweinswal_2010.jpg" alt="Vorschaugrafik" />
