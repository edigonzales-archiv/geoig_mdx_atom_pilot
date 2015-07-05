DROP TABLE fts_metadb;
CREATE VIRTUAL TABLE fts_metadb USING fts3(id INTEGER PRIMARY KEY, m_pkuid, identifier, namespace, title, abstract, canton, data_responsibility, d_pkuid, uri, format_mime, format_txt, srs_epsg, srs_txt, modified);
INSERT INTO fts_metadb(id, m_pkuid, identifier, namespace, title, abstract, canton, data_responsibility, d_pkuid, uri, format_mime, format_txt, srs_epsg, srs_txt, modified) SELECT d.rowid, m.pkuid as m_pkuid, m.identifier, m.namespace, m.title, m.abstract, m.canton, m.data_responsibility, 
  d.pkuid as d_pkuid, d.uri, d.format_mime, d.format_txt, d.srs_epsg, d.srs_txt, d.modified
  FROM metadb m, online_dataset d
  WHERE m.identifier = d.metadb_id
  AND m.type = 100;

--DELETE FROM fts_metadb;

SELECT rowid, * FROM fts_metadb WHERE fts_metadb MATCH '2480 2056';

select * from fts_metadb
