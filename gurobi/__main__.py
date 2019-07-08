#!python3
# https://nagios-plugins.org/doc/guidelines.html

# Import required libs for sharepointhealth
from .gurobi_check import GurobiMachines
import argparse
import sys
import arrow


# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Return message
message = {
    'status': OK,
    'summary': 'Example summary',
    'perfdata': 'label1=0;;;; '  # 'label'=value[UOM];[warn];[crit];[min];[max] 
}

# For multiple perdata, ensure to add space after each perfdata
# message['perfdata'] = 'label1=x;;;; '
# message['perfdata'] += 'label2=x;;;; '

# Function to parse arguments
def parse_args(args):
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
     https://docs.python.org/3/library/argparse.html
    :return: parse.parse_args(args) object
    You can use obj.option, example:
    options = parse_args(args)
    options.user # to read username
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
                                     description='nagios plugin to check some url using curl and some other code')

    parser.add_argument('-u', '--url', dest='url', nargs='?', default=None, const=None,
                        help='url to check \n')
    parser.add_argument('-e', '--extra_args', dest='extra_args', nargs='?', default='', const=None,
                            help='extra args to add to curl, see curl manpage  \n')
    parser.add_argument('--client_id', dest='client_id', nargs='?', default=None, const=None,
                            help='Header client_id \n')
    parser.add_argument('--client_secret', dest='client_secret', nargs='?', default=None, const=None,
                            help='Header client_secret  \n')
    parser.add_argument('--outdated_minutes', dest='outdated_minutes', type=int , nargs='?', default=60, const=None,
                            help='Minutes to consider outdated  \n')

    if not args:
        raise SystemExit(parser.print_help())

    return parser.parse_args(args)

# Function to execute cli commands
def cli_execution(options):
    """
    : param: options: arguments from parse.parse_args(args) (see parse_args function)
    """
    #variables
    auth_args = ''
    machine_names=''
    retrcode = OK
    
    if not options.client_id:
            sys.exit('param client_id is required  when using gurobi check ')
    if not options.client_secret:
            sys.exit('param client_secret is required  when using gurobi check ')

    gurobi_obj = GurobiMachines(url= options.url,
                                   client_id = options.client_id,
                                   client_secret = options.client_secret)	

    gurobi_tuple = gurobi_obj.get_machines(machine_names)
    
    auth_http_code = gurobi_tuple[1]
    if auth_http_code != 200:
            sys.exit('Error getting data from {} http_code != 200, http_code: {}'.format(options.url, 
                                                                                         auth_http_code))

    def check_data():
        # use new object class HealthMonitor
        retrcode, machine_names = gurobi_obj.check_machines(options.outdated_minutes)
        return retrcode, machine_names
    
    def format_message():
        return 'url: {} '.format(options.url)

    def check(retrcode):
        if retrcode == 2:
            status = CRITICAL
            message['summary'] = 'CRITICAL: '
        else:
            status = OK
            message['summary'] = 'OK: '
        return status

    # Check logic starts here
    data_code, machine_dates_list = check_data()
    message['status'] = check(data_code)
    # Add summary    
    message['summary'] += format_message()
    message['summary'] += str(machine_dates_list)
    # Add perfdata
    total = len(machine_dates_list)
    message['perfdata'] = 'total machines={};;1;; '.format(total)

    # Print the message
    print("{summary}|{perfdata}".format(
        summary=message.get('summary'),
        perfdata=message.get('perfdata')
    ))

    # Exit with status code
    raise SystemExit(message['status'])

# Argument parser
# https://docs.python.org/3.5/library/argparse.html

def main():
    """
    Main function
    """
    # Get options with argparse
    options = parse_args(sys.argv[1:])
    # Execute program functions passing the options collected
    cli_execution(options)


if __name__ == "__main__":
    main()
