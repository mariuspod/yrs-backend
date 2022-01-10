from pony.orm import *
import os

def connect_db():
  db = Database()
  db_host = os.environ['DB_HOST']
  db_port = os.environ['DB_PORT']
  db_user = os.environ['DB_USER']
  db_pass = os.environ['DB_PASS']
  db_name = os.environ['DB_NAME']

  db.bind(provider='postgres', user=db_user, password=db_pass, host=db_host, port=db_port, database=db_name)
  return db
