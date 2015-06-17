INSERT INTO "type" (code, code_txt) VALUES (0, 'undefined');
INSERT INTO "type" (code, code_txt) VALUES (1, 'root');
INSERT INTO "type" (code, code_txt) VALUES (100, 'dataset');
INSERT INTO "type" (code, code_txt) VALUES (200, 'wms');
INSERT INTO "type" (code, code_txt) VALUES (210, 'wmts');
INSERT INTO "type" (code, code_txt) VALUES (220, 'wfs');
INSERT INTO "type" (code, code_txt) VALUES (230, 'wcs');
INSERT INTO "type" (code, code_txt) VALUES (500, 'postgres');


INSERT INTO metadb (identifier, title, abstract, "type") VALUES ('ea5c61e7-1be8-4c3f-b7aa-4aa4f35072db', 'Stromversorgungssicherheit: Netzgebiete', 'Netzgebiete, der auf dem Gebiet des Kantons Glarus tätigen Netzbetreiber gemäss Artikel 5 Absatz 1 StromVG.', 1);
INSERT INTO metadb (identifier, title, abstract, "type", modified, x_min, y_min, x_max, y_max) VALUES ('9565af3d-9d96-44bb-a9f8-de8e405c56f3', 'Stromversorgungssicherheit: Netzgebiete', 'Netzgebiete, der auf dem Gebiet des Kantons Glarus tätigen Netzbetreiber gemäss Artikel 5 Absatz 1 StromVG.', 1, '2015-04-01 06:00:00', 8.87124, 46.7965, 9.25259, 47.174);
INSERT INTO metadb (identifier, title, abstract, "type", modified, x_min, y_min, x_max, y_max) VALUES ('25701ebd-0464-480e-917f-3151eb5ddb8c', 'Dummy zum Testen der Abfrage und das Erstellen der XML-Dateien.', 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.', 1, '2015-05-03 07:00:00', 7.87124, 46.7965, 8.25259, 47.174);


INSERT INTO metadb_relation (metadb_id_parent, metadb_id_child) VALUES ('ea5c61e7-1be8-4c3f-b7aa-4aa4f35072db', '9565af3d-9d96-44bb-a9f8-de8e405c56f3');
INSERT INTO metadb_relation (metadb_id_parent, metadb_id_child) VALUES ('ea5c61e7-1be8-4c3f-b7aa-4aa4f35072db', '25701ebd-0464-480e-917f-3151eb5ddb8c');


INSERT INTO online_dataset (metadb_id, uri, format_mime, format_txt, srs_epgs, srs_txt, modified) VALUES ('9565af3d-9d96-44bb-a9f8-de8e405c56f3', 'http://www.catais.org/geodaten/ch/gl/efs/9565af3d-9d96-44bb-a9f8-de8e405c56f3_LV03_xtf.xtf', 'text/x-interlis23', 'INTERLIS23', '21781', 'LV03', '2015-04-01 06:00:00');
INSERT INTO online_dataset (metadb_id, uri, format_mime, format_txt, srs_epgs, srs_txt, modified) VALUES ('9565af3d-9d96-44bb-a9f8-de8e405c56f3', 'http://www.catais.org/geodaten/ch/gl/efs/9565af3d-9d96-44bb-a9f8-de8e405c56f3_LV03_gml.gml', 'application/gml+xml;version=3.2', 'GML 3.2.1', '21781', 'LV03', '2015-04-01 06:00:00');
