import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import os
import contextlib
import json

# with contextlib.suppress(FileNotFoundError): os.unlink("test.sql")

# def prerunsql(x):
#     e = sqlalchemy.create_engine("sqlite:///test.sql")
#     with e.connect() as c:
#         c.exec_driver_sql(x)
#         c.commit()
#         c.close()

# prerunsql("CREATE TABLE test(id integer primary key, name text);")


#src_engine = sqlalchemy.create_engine("sqlite:///test.sql")

mysql_user = os.getenv("DBUSER")
mysql_pass = os.getenv("DBPASS")
mysql_host = os.getenv("DBHOST")
mysql_port = os.getenv("DBPORT")
mysql_name = os.getenv("DBNAME")
mysql_cafilename = os.getenv("DBCAFILENAME")

mysqlconstr = "mysql+pymysql://%s:%s@%s:%s/%s" % (mysql_user, mysql_pass, mysql_host, mysql_port, mysql_name)

src_engine = sqlalchemy.create_engine(mysqlconstr)



Src_Base = sqlalchemy.ext.automap.automap_base()
src_session = sqlalchemy.orm.Session(src_engine)

Src_Base.prepare(autoload_with=src_engine)




src_metadata = sqlalchemy.MetaData()
src_metadata.reflect(bind=src_engine)


for x in src_metadata.sorted_tables:
    print(x)


# t_test = Src_Base.classes.table1

# x = t_test(name="oink")
# src_session.add(x)
# src_session.commit()
