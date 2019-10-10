
  # Controller
  
  #### Database Connection
  check this video out [psycopg2](https://www.youtube.com/watch?v=_vqXqPVo68o)
  
  without the database connection file, the controller have 5 files:
  1. run.py
  2. Task.py
  3. Experiment.py
  4. NodeThread.py
  5. ControllerManager.py
  
  
  Check out the Node tutorial to know what run.py do, and socketserver
  The only difference here, ( i mean about run.py ) , is that the node have a signal handling, but the controller dont, the controller have a bootup method, that check if it can connect to the node, ( the bootup method not the bootup_thread method, its better to testboth )
  
  #### controller manager
  
  it run on separete thread, check out my python multithread example to know how multitheaded work in python
  
  it has a couple of methods, and a lot of attribute ( why not increase memory !!)
  1. setup node
  2. set_cordy
  3. run
  4. setup_experiment
  5. read_start
  6. sensor
  7. add_Experiment
  8. parse
  9. get_experiment
  10. close
  
  
  because the manager is running on separe thread, the run method will be called, whenever you do manager.start ( line 110 in run.py )
  
  but when you create the object of the class, it will first run _ _ init _ _ method, which will run setup_node and this method try to connect each node, and get the status out of it ( the controller assume that the node is already running )
  
  then when the main thread reach line 110 and manager start, it will try to identify the coordinator ( in zigbee the coordinator is a property so it can be 1 or 0 )
  
  and then the controller wait, untill the queue is filled with experiment,
  
  now the information about the experiment collected in the webinterface, then the number ( id of experiment ) passed to the queue ( run.py add line 76 )
  
  then the controller will fetch the information directly from the database ( again bad design ) and start the experiment, and here come the role of experiment.py and task.py
  
  experiment.py hold information about the experiment ( status , and other things in the database )
  however now that i have checked the code, task class is not used in the controller
  
  read_start is probably the worst method i have ever written, it so slow !!!
  
  however it's alot easier to understand 
'''
tags: []
isStarred: false
isTrashed: false
