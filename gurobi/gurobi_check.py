#
# documentation:
import requests
import json
import arrow

# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

class GurobiMachines:
    def __init__(self, url, client_id, client_secret):
        
        #initial
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret

    def get_machines(self, machine_name=''):
        
        # Request JSON machines
        headers = {'accept': 'application/json',
            'X-GUROBI-ACCESS-ID': '{}'.format(self.client_id),
            'X-GUROBI-SECRET-KEY': '{}'.format(self.client_secret)}
        
        # Request to get machine names or machines created time
        # Get machines names if the machine is not defined or get the details of machine if is defined.
        # https://cloud.gurobi.com/swagger.html#/Pools/post_pools__poolId__machines
        if machine_name == '':
            url = self.url
        else:
            url = 'https://cloud.gurobi.com/api/v2/machines/' + '{}'.format(machine_name)

        # requests doc http://docs.python-requests.org/en/v0.10.7/user/quickstart/#custom-headers
        r = requests.get(url=url, headers=headers)
        
        return r.json(), r.status_code
    
    def check_machines(self, outdated_minutes):

        #variables
        retrcode = OK
        actual_time = arrow.get()
        outdated_time = actual_time.shift(minutes=-outdated_minutes)
        machines_dates = []
        
        #Get current machines names
        machines_tuple = self.get_machines()
        machines_list = machines_tuple[0]
        computeServers = machines_list.get('computeServers')

        if computeServers:
            for item in computeServers:
                machine_name = item.get('machineId', '')
        
                #Get machines created time and compare with outdated_time
                if machine_name != '':
                    machines_details_tuple = self.get_machines(machine_name)
                    machines_details_list = machines_details_tuple[0]
                    machine_createdAt  = arrow.get(machines_details_list.get('createdAt'))
                    if machine_createdAt < outdated_time:
                        retrcode = CRITICAL
                        machine_createdAt_raw = machines_details_list.get('createdAt', '')
                        machines_dates.append('machine: {}, date: {}'.format(machine_name, machine_createdAt_raw))

        return retrcode, machines_dates
