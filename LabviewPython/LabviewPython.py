import socket
import json
class LVconnection():

    def __init__(self):
        self.conn = None
    def recv_data(self):
        assert(self.conn!=None)
        buffer = ''
        while True:
            try:
                #read from the connection until CRLF
                #self.conn.settimeout(0.5) #set the timeout to 500 ms
                rtrn_msg = self.conn.recv(1024).decode("utf-8")
                buffer+=rtrn_msg
                if r'\r\n' in buffer:
                    buffer = buffer.replace(r'\r\n','')
                    break
            except Exception as e:
                print('Warming: message not received, Error:{}'.format(e))
                break
        return buffer

    def send_data(self,data):
        assert(self.conn!=None)
        self.conn.sendall(bytes(data+'\r\n','utf-8'))
    def connect(self): #connect to server
        assert(self.conn==None)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 8089)
        client.connect(server_address)
        #client.setblocking(0) #this will allow the recv method to timeout
        self.conn = client
    def close(self): #close connection to server
        assert(self.conn!=None)
        #self.conn.shutdown('SHUT_RDWR')
        self.conn.close()
        self.conn = None
class LVfunctions():
    def __init__(self):
        self.LVconn = LVconnection()
    def testing(self):
        data = {
            'Command':'Testing',
            'Data':'This is a test'
            }
        msg = json.dumps(data)
        self.LVconn.connect()
        self.LVconn.send_data(msg)
        recv_msg = self.LVconn.recv_data()
        print(recv_msg)
        recv_data = json.loads(recv_msg)
        print(recv_data['Data'])
        self.LVconn.close()
    def get_mass(self,scan_info_in,data_in):
        scan_info = {
            'High Frequency (Hz)':list(scan_info_in['High Frequency (Hz)']),
            'Low Frequency (Hz)':list(scan_info_in['Low Frequency (Hz)']),
            'Peak Width':list(scan_info_in['Peak Width']),
            'Peak Amplitude':list(scan_info_in['Peak Amplitude']),
            'Fit Position (Hz)':list(data_in['Fit Position (Hz)'])
            }
        data={
            'Time (s)':list(data_in['Time (s)']),
            'Fit Position (Hz)':list(data_in['Fit Position (Hz)']),
            'Mass To Charge (kg/e)':[x*1.6605390666E-27 for x in data_in['Mass To Charge (Da/e)']],#need to convert from Da to kg
            'Q Step Threshold (Hz)':data_in['Q Step Threshold (Hz)'],
            'Q step procedure Start Time (s)':data_in['Q step procedure Start Time (s)'],
            'Q step procedure End Time (s)':data_in['Q step procedure End Time (s)'],
            'Scan Information':scan_info
            }
        msg_in={
			'Command':'get_mass',
			'Data':json.dumps(data)
            }
        self.LVconn.connect()
        self.LVconn.send_data(json.dumps(msg_in))
        msg_out = self.LVconn.recv_data()
        data_out = json.loads(msg_out)
        self.LVconn.close()
        data_out = {
            'Time (s)': data_out['Time (s)'],
            'Mass (Da)': [x/1.6605390666E-27 for x in data_out['Mass (kg)']],
            'Charge (e)': data_out['Charge (e)'],
            'Mass/Charge (Da/e)': [x/1.6605390666E-27 for x in data_out['Mass/Charge (kg/e)']]
            }
        return data_out
    def filter_mass_data(self,data_in):
        '''
        parameters
        ----------
        data : Dictionary of arrays and floats
            keys:
                High Frequency (Hz): ``list(float)``:
                Low Frequency (Hz): ``list(float)``:
                Peak Width: ``list(float)``:
                Peak Amplitude: ``list(float)``:
                UV Lamp: ``list(float)``:
                Time (s): ``list(float)``:
                Fit Position (Hz): ``list(float):
                Mass To Charge (Da/e): ``list(float):
                Charge (e): ``list(float):
                Window Size: ``float``:
                Max Sweep Range: ``float``:

        '''
        data = {
            'High Frequency (Hz)':list(data_in['High Frequency (Hz)']),
            'Low Frequency (Hz)':list(data_in['Low Frequency (Hz)']),
            'Peak Width':list(data_in['Peak Width']),
            'Peak Amplitude':list(data_in['Peak Amplitude']),
            'UV Lamp':list(data_in['UV Lamp']),

            'Time (s)':list(data_in['Time (s)']),
            'Fit Position (Hz)':list(data_in['Fit Position (Hz)']),
            'Mass To Charge (kg/e)':[x*1.6605390666E-27 for x in list(data_in['Mass To Charge (Da/e)'])],
            'Charge (e)':list(data_in['Charge (e)']),
            'Window Size':data_in['Window_Size'],
            'Max Sweep Range':data_in['Max Sweep Range']
            }
        msg_in={
            'Command':'filter_mass_data',
            'Data':json.dumps(data)
            }
        self.LVconn.connect()
        self.LVconn.send_data(json.dumps(msg_in))
        msg_out = self.LVconn.recv_data()
        data_out = json.loads(msg_out)
        self.LVconn.close()
        data_out = {
            'Time (s)':list(data_out['Time (s)']),
            'Fit Position (Hz)':list(data_out['Fit Position (Hz)']),
            'Mass/Charge (Da/e)':[x/1.6605390666E-27 for x in list(data_out['Mass/Charge (kg/e)'])],
            'Index':list(data_out['Index'])
            }
        return data_out
    def get_charge(self,data_in):
        data={
            'Q Step Threshold (Hz)':data_in['Q Step Threshold (Hz)'],
            'Time (s)':list(data_in['Time (s)']),
            'Fit Position (Hz)':list(data_in['Fit Position (Hz)']),
            'Mass To Charge (kg/e)': [x*1.6605390666E-27 for x in list(data_in['Mass To Charge (Da/e)'])]
            }
        msg_in={
            'Command':'get_charge',
            'Data':json.dumps(data)
            }
        self.LVconn.connect()
        self.LVconn.send_data(json.dumps(msg_in))
        msg_out = self.LVconn.recv_data()
        data_out = json.loads(msg_out)
        self.LVconn.close()
        data_out = {
            'Charge (e)':list(data_out['Charge (e)']),
            'Mass (Da)':[x/1.6605390666E-27 for x in list(data_out['Mass (kg)'])],
            'Ending Charge (e)':data_out['Ending Charge (e)']
            }
        return data_out
    def closest_mass(self,data_in):
        '''
        Parameters
        ----------
        data_in : Dictionary of arrays or float values
            keys:
                Time (s):``list(float):
                Start Q (e):``float``:
                Mass To Charge (Da/e):``list(float):
        Returns
        -------
        data_out : Dictionary of arrays or float values
        '''
        data={
            'Time (s)':list(data_in['Time (s)']),
            'Start Q':data_in['Start Q (e)'],
            'Mass To Charge (kg/e)':[x*1.6605390666E-27 for x in list(data_in['Mass To Charge (Da/e)'])]
            }
        msg_in={
            'Command':'closest_mass',
            'Data':json.dumps(data)
            }
        self.LVconn.connect()
        self.LVconn.send_data(json.dumps(msg_in))
        msg_out = self.LVconn.recv_data()
        data_out = json.loads(msg_out)
        self.LVconn.close()
        data_out = {
            'Charge (e)': data_out['Charge (e)'],
            'Mass (Da)':[x/1.6605390666E-27 for x in list(data_out['Mass (kg)'])]
            }
        return data_out
