import psycopg2 as p
import psycopg2.extras as e
import json



class DatabaseConnection(object):
	def __init__(self):
		self.con = p.connect("dbname='berrybed' user='berrybed' password='1234' host='localhost'")
		self.con.autocommit = True
		self.cur = self.con.cursor(cursor_factory=e.RealDictCursor)


	def get_Experiment_info(self,eid):
		stmt = 'SELECT * FROM experiments WHERE eid=' + str(eid)
		self.cur.execute(stmt)
		result = self.cur.fetchall()
		return result[0]

	def change_to_running(self,eid):
		stmt = "UPDATE experiments SET status='running' WHERE eid=" +str(eid)
		self.cur.execute(stmt)


	def change_to_done(self,eid):
		stmt = "UPDATE experiments SET status='done' WHERE eid=" +str(eid)
		self.cur.execute(stmt)

	def get_Node_info(self,eid):
		stmt = "SELECT * FROM nodes WHERE eid=" + str(eid)
		self.cur.execute(stmt)
		result = self.cur.fetchall()
		return result

	def get_scenario_info(self,eid):
		stmt = "SELECT * FROM scenario WHERE eid=" + str(eid)
		self.cur.execute(stmt)
		result = self.cur.fetchall()
		return result

	def get_node_name(self,nid):
		stmt = "SELECT * FROM nodes WHERE nid=" +str(nid)
		self.cur.execute(stmt)
		result = self.cur.fetchall()
		return result[0]['name']

	def save_results(self,pid,eid,output):
		values = {
			"pid" : str(pid),
			"eid" : str(eid),
			"output" : str(output)

		}
		self.cur.execute("""INSERT INTO results(pid,eid,output) VALUES(%(pid)s,%(eid)s,%(output)s)""",values)

