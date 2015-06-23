#!/bin/bash

SUPERUSER="stefan"

ADMIN="stefan"
ADMINPWD="ziegler12"
USER="mspublic"
USERPWD="mspublic"

DB_NAME="xanadu"

echo "Delete database: $DB_NAME"
sudo -u $SUPERUSER dropdb $DB_NAME

echo "Create database: $DB_NAME"
sudo -u $SUPERUSER createdb --owner $ADMIN $DB_NAME

echo "Load postgis"
sudo -u $SUPERUSER psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
#sudo -u $SUPERUSER psql -d $DB_NAME -c "CREATE EXTENSION pointcloud;"
#sudo -u $SUPERUSER psql -d $DB_NAME -c "CREATE EXTENSION pointcloud_postgis;"


echo "Grant tables to..."
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $ADMIN;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "ALTER TABLE geometry_columns OWNER TO $ADMIN;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON geometry_columns TO $ADMIN;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON spatial_ref_sys TO $ADMIN;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON geography_columns TO $ADMIN;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON raster_columns TO $ADMIN;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON raster_overviews TO $ADMIN;"
#sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON pointcloud_columns TO $ADMIN;"
#sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT ALL ON pointcloud_formats TO $ADMIN;"

sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT SELECT ON geometry_columns TO $USER;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT SELECT ON spatial_ref_sys TO $USER;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT SELECT ON geography_columns TO $USER;"
sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT SELECT ON raster_columns TO $USER;"
#sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT SELECT ON pointcloud_columns TO $USER;"
#sudo -u $SUPERUSER psql -d $DB_NAME -c "GRANT SELECT ON pointcloud_formats TO $USER;"