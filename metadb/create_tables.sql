-- Zuständigkeit (Namen)
-- "considered" default dataset...
-- Thema (um auch noch nach Thema abzufragen).


CREATE TABLE metadb
(
  pkuid integer NOT NULL,
  identifier varchar NOT NULL,
  namespace varchar,
  title varchar NOT NULL,
  abstract varchar,
  metadata_link varchar,
  "type" integer NOT NULL,
  modified datetime,
  canton varchar,
  data_responsibility varchar,
  x_min float,
  y_min float,
  x_max float,
  y_max float, 
  PRIMARY KEY ("pkuid")
);

CREATE TABLE metadb_relation
(
  pkuid integer NOT NULL,
  metadb_id_parent varchar NOT NULL,
  metadb_id_child varchar NOT NULL,
  PRIMARY KEY ("pkuid")
);


CREATE TABLE online_dataset
(
  pkuid integer NOT NULL,
  metadb_id varchar NOT NULL,
  uri varchar NOT NULL,
  format_mime varchar NOT NULL,
  format_txt varchar NOT NULL,
  srs_epsg integer NOT NULL,
  srs_txt varchar,
  modified datetime NOT NULL,  
  PRIMARY KEY ("pkuid")
);

CREATE TABLE online_service
(
  pkuid integer NOT NULL,
  metadb_id varchar NOT NULL,
  uri varchar NOT NULL,
  PRIMARY KEY ("pkuid")
);

CREATE TABLE "type"
(
  pkuid integer NOT NULL,
  code integer NOT NULL,
  code_txt varchar NOT NULL,
  PRIMARY KEY ("pkuid")
);
