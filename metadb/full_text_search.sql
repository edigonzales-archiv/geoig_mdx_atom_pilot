DROP TABLE fts_metadb;
CREATE VIRTUAL TABLE fts_metadb USING fts3(m_pkuid, identifier, title, abstract, canton, data_responsibility, d_pkuid, format_mime, format_txt, srs_epsg, srs_txt);
INSERT INTO fts_metadb SELECT m.pkuid as m_pkuid, m.identifier, m.title, m.abstract, m.canton, m.data_responsibility, 
  d.pkuid as d_pkuid, d.format_mime, d.format_txt, d.srs_epsg, d.srs_txt
  FROM metadb m, online_dataset d
  WHERE m.identifier = d.metadb_id
  AND m.type = 100;

--DELETE FROM fts_metadb;

SELECT * FROM fts_metadb WHERE fts_metadb MATCH '2480 2056';

