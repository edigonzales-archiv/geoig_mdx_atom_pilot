#!/bin/bash

SUPERUSER="stefan"

#ADMIN="stefan"
#ADMINPWD="ziegler12"
USER="mspublic"
USERPWD="mspublic"

echo "Create database user"
#sudo -u $SUPERUSER psql -d postgres -c "CREATE ROLE $ADMIN CREATEDB LOGIN PASSWORD '$ADMINPWD';"
#sudo -u $SUPERUSER psql -d postgres -c "CREATE ROLE $USER LOGIN PASSWORD '$USERPWD';"
sudo -u $SUPERUSER psql -d postgres -c "CREATE ROLE $USER LOGIN PASSWORD '$USERPWD';"