CREATE TABLE amtliche_vermessung
(
  pkuid integer NOT NULL,
  bfsnr integer NOT NULL,
  canton varchar NOT NULL,
  gem_name varchar NOT NULL,
  updated datetime NOT NULL,
  imported datetime NOT NULL,
  spatial_dataset_identifier_code varchar NOT NULL,
  spatial_dataset_identifier_namespace varchar NOT NULL,
  mime_type varchar NOT NULL,
  crs varchar NOT NULL,
  service_feed varchar NOT NULL,  
  path varchar NOT NULL,
  PRIMARY KEY ("pkuid")
);

INSERT INTO amtliche_vermessung (bfsnr, canton, gem_name, updated, imported, spatial_dataset_identifier_code, spatial_dataset_identifier_namespace, mime_type, crs, service_feed, path) VALUES (2549, 'so', 'Kammersrohr', '2015-04-01 06:00:00', '2015-04-01 06:00:00', '51f3f236-9ed5-424e-b201-93998801d7c2', 'http://www.geo.so.ch', 'text/x-interlis1', 'http://www.opengis.net/def/crs/EPSG/0/21781', 'http://www.catais.org/geoig/services/dls/ch/so/agi/service.xml', '/tmp/ch_254900.itf');

INSERT INTO amtliche_vermessung (bfsnr, canton, gem_name, updated, imported, spatial_dataset_identifier_code, spatial_dataset_identifier_namespace, mime_type, crs, service_feed, path) VALUES (2524, 'so', 'Hüniken', '2015-04-01 06:00:00', '2015-04-01 06:00:00', '0c98aa82-4974-4b65-beb2-c32789b20697', 'http://www.geo.so.ch', 'text/x-interlis1', 'http://www.opengis.net/def/crs/EPSG/0/21781', 'http://www.catais.org/geoig/services/dls/ch/so/agi/service.xml', '/tmp/ch_252400.itf');