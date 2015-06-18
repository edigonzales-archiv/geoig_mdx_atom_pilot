-- Mich interessieren mit nur die Versorgungsgebiete.
-- Dazu muss ich den root-identifier kennen für die Fälle, 
-- wo es keine 1:1-Beziehung ist. Z.B. amtliche Vermessung
-- (gemeindeweise).

SELECT m.*
FROM metadb as m, 
(
  SELECT  * 
  FROM metadb_relation 
  WHERE metadb_id_parent = 'ea5c61e7-1be8-4c3f-b7aa-4aa4f35072db'
 ) as r
WHERE m.identifier = r.metadb_id_child
ORDER BY m.title;

-- Oder: alles was ein 'dataset' ist:
SELECT *
FROM metadb
WHERE "type" == 100