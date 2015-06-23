# MDX: Pilotprojekt Atom/OpenSearch

## Datenimport

```
java -jar /home/stefan/Projekte/geoig_mdx_atom_pilot/ili2pg/ili2pg-2.1.4/ili2pg.jar --import --dbhost localhost --dbport 5432 --dbusr stefan --dbpwd ziegler12 --dbdatabase xanadu2_test --dbschema supplysecurity --createGeomIdx --strokeArcs --nameByTopic --createEnumTabs --models SupplySecurity_RuledAreas_V1 supplysecurity.xtf

```
(Datenimport nicht notwendig.)

## virtualenv (inkl. flask)

### virtualenv installieren

```
sudo apt-get install python-pip
sudo pip install virtualenv virtualenvwrapper
```

In `.bashrc` einfügen:

```
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
fi
```

### Projekt clonen

```
git clone https://edigonzales@bitbucket.org/edigonzales/fuuuuuuuuuuuuuuuuuuuuuuuuuu
```

### virtualenv einrichten

```
virtualenv venv
source venv/bin/activate
pip install flask
pip install pytz
pip install psycopg2
```

`psycopg2` nur für das Erstellen der INSERT-SQL-Kommandos der amtlichen Vermessung.

### Apache config file

```
WSGIScriptAlias /geoig/services /home/stefan/Projekte/geoig_mdx_atom_pilot/services/wsgi/flask.wsgi
WSGIScriptReloading On

<Directory /home/stefan/Projekte/geoig_mdx_atom_pilot/services/wsgi>
    Order deny,allow
    Allow from all
</Directory>
```

### Develop mode (local web server)
Als erste Zeile in von `run.py`: `#!venv/bin/python`

Und zu guter letzt:

```
if __name__ == '__main__':
    app.run(debug=True)
```
