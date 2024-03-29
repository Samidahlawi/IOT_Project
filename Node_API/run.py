from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from config import ConfigAddress

#import config

app = Flask(__name__)
api = Api(app)

###############
## paths
# /devise_Info => to get the information of the device and what device have of attchements 
# /device/readdata => 
###############

### temporary variables 
first_time_run = True
set_time = ''

# This class for request and response for device information 
class DeviceInfo(Resource):
	# wlan0 for interface of wifi in the raspberryPi 
	address = ConfigAddress()
	mac_address = address.get_mac_address('wlan0')
	ip_address  = address.get_ip_address() 
	# function will return json about informatin of device 
	def get(self):
		global first_time_run, set_time

		if (first_time_run):
		    set_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		    first_time_run = False
		return {
			"ip_address":self.ip_address,
			"id":self.mac_address,
			"start_Run":set_time,
			"attachments":"['temperature sensor','Humidity sensor']",
			"power_supply":"Battery",
			"device_type":"Raspberry PI"
			},200


# GET - /device_info => to get details of the device
api.add_resource(DeviceInfo,'/device_info')



if __name__ == '__main__':
	app.run(host='0.0.0.0',port=9090)


