import requests

class IR_Transceiver():

    def __init__(self, device_id, access_token):
        self.device_id = device_id
        self.access_token = access_token

    def getIR(self):
        # Enable IR receiver on device
        r = requests.post(r'https://api.particle.io/v1/devices/%s/getIR' % self.device_id, data={'access_token': self.access_token})
        if 'error' in r.text:
            return -1
        # Get returned IR data
        ir_code = ''
        while (ir_code == ''):
            r = requests.get(r'https://api.particle.io/v1/devices/%s/getIR_data?access_token=%s' % (self.device_id, self.access_token))
            if 'error' in r.text:
                return False
            else:
                ir_code = r.json()['result']
        return ir_code

    def sendIR(self, ir_code):
        r = requests.post(r'https://api.particle.io/v1/devices/%s/sendIR' % self.device_id, data={'args': ir_code, 'access_token': self.access_token})
        if 'error' in r.text:
            return False
        else:
            return True
