# pip install git+https://github.com/WPSemantix/timbr_python_SQLAlchemy
from sqlalchemy.engine import create_engine
from TCLIService.ttypes import TOperationState

if __name__ == '__main__':
  # HTTPS example

  hostname = 'staging.timbr.ai'
  port = '443'
  protocol = 'https'
  ontology = 'timbr_e2e_tests'
  username = 'token'
  password = 'tk_f283d1885598e6a79b7a56265484174e709c73d72abdaaa0025990a43f4e981d'




  # # example file

  # # Create new sqlalchemy connection
  # engine = create_engine(f"timbr+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}")
  
  # # Connect to the created engine
  # conn = engine.connect()
  
  # # Execute a query
  # query = "SHOW CONCEPTS"
  # concepts = conn.execute(query).fetchall()
  
  # # Display the results of the execution
  # for concept in concepts:
  #   print(concept)




  # async pyhive

  # Create new sqlalchemy connection
  engine = create_engine(f"hive+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}", connect_args={'configuration': {'set:hiveconf:hiveMetadata': 'true'}})

  # Connect to the created engine
  conn = engine.connect()
  dbapi_conn = engine.raw_connection()
  cursor = dbapi_conn.cursor()

  # Execute a query
  query = "SHOW CONCEPTS"
  cursor.execute(query)

  # Check the status of this execution
  status = cursor.poll().operationState
  while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
    status = cursor.poll().operationState

  # Display the results of the execution
  results = cursor.fetchall()
  print(results)





  # # sync pyhive

  # # Create new sqlalchemy connection
  # engine = create_engine(f"hive+{protocol}://{username}@{ontology}:{password}@{hostname}:{port}", connect_args={'configuration': {'set:hiveconf:async': 'false', 'set:hiveconf:hiveMetadata': 'true'}})

  # # Connect to the created engine
  # conn = engine.connect()

  # # Use the connection to execute a query
  # query = "SHOW CONCEPTS"
  # results = conn.execute(query).fetchall()

  # # Display the results of the execution
  # print(results)