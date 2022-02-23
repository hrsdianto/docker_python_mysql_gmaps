#create virtual enviroment
py -m venv myenv

#activate myenv
.\myenv\Scripts\activate

#install package moduls
pip3 install requests
pip3 install mysql-connector-python
pip3 install schedule
pip3 freeze > requirements.txt

#creat valume
docker volume create mysql_py
docker volume create mysql_config_py

#create network
docker network create mysqlnet_py

#run MySQL in a container
docker run --rm -d -v mysql_py:/var/lib/mysql \
-v mysql_config_py:/etc/mysql \
-p 3306:3306 \
--network mysqlnet_py \
--name mysqldb \
-e MYSQL_ROOT_PASSWORD=321 \
mysql

#make sure mysqldb is running 
docker exec -ti mysqldb mysql -u root -p
mysql>USE db_traffic;
mysql>SHOW TABLES;
mysql>SELECT * FROM traffic;

#setup timezone in mysql for you current location
mysql>SET GLOBAL time_zone = "Asia/Jakarta";
mysql>SET time_zone = "+07:00";
mysql>SET @@session.time_zone = "+07:00";

#instal package modul app
pip3 install mysql-connector-python
pip3 freeze | grep mysql-connector-python >> requirements.txt

#run create_db.py
#run insert_db.py --> modified routes information 
#run delete_db.py --> optional