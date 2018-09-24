#!/bin/bash
#Instalacion

cd ~
apt-get update
#apt-get upgrade
pip install django==1.11.5
# pip install django-googleplay-api # (ver configuracion que esta en ruso)
# sed -i "s/LANG = get_settings('LANG', \"ru_RU\")/LANG = get_settings('LANG', \"es_AR\")/" /usr/local/lib/python2.7/dist-packages/djgpa/configs.py 
# sed -i "s/COUNTRY = get_settings('COUNTRY', 'ru')/COUNTRY = get_settings('COUNTRY', 'ar')/" /usr/local/lib/python2.7/dist-packages/djgpa/configs.py 

pip install androguard
pip install python-dateutil
pip install pika
pip install python-gitlab
apt-get -y install cmake
apt-get -y install python-cffi
apt-get -y install python-dev
apt-get -y install rabbitmq-server


# Instalación libgit2
wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
tar xvzf v0.27.0.tar.gz
cd libgit2-0.27.0
cmake .
make
make install
ldconfig
cd ..
rm -rf libgit2-0.27.0

# Instalación pygit2
wget https://github.com/libgit2/pygit2/archive/v0.27.0.tar.gz
tar xvzf v0.27.0.tar.gz
cd pygit2-0.27.20
python setup.py install
cd ..
rm -rf pygit2-0.27.0

# Instalación mySQL
apt-get -y install mysql-server
apt-get -y install mysql-client
apt-get -y install libmysqlclient-dev
#mysql -u root -p < init_database.sql
pip install mysql-python
pip install simplejson
pip install arff
apt-get -y install openjdk-7-jdk

# Instalación Bungiesearch
wget https://github.com/ChristopherRabotin/bungiesearch/archive/v1.2.2.tar.gz
tar xvzf v1.2.2.tar.gz
cd bungiesearch-1.2.2
python setup.py install
cd ..
rm -rf bungiesearch-1.2.2

apt-get -y install weka

# Instalación elasticsearch
wget https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.1.0/elasticsearch-2.1.0.deb
dpkg -i elasticsearch-2.1.0.deb
service elasticsearch start
update-rc.d elasticsearch defaults 95 10
# El marvin-static-analyzer hay que bajarlo con un usuario raso
# git clone https://jheguia@bitbucket.org/jrinaudo/marvin-static-analyzer.git


