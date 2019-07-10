Gurobi monitoring plugin
========================

Checks an url raise an alert if some problem is found.
Uses curl with all its power, so you can extend your check with all curl options.

`VERSION  <burp_reports/VERSION>`__

Install
=======

Linux::

    sudo pip3 install gurobi_machines_plugin --upgrade

Also is possible to use::

    sudo python3 -m pip install gurobi_machines_plugin --upgrade

On windows with python3.5::

    pip install gurobi_machines_plugin --upgrade

For proxies add::

    --proxy='http://user:passw@server:port'

Usage
=====

Use the command line::

    > gurobi_machines_plugin --help
      usage: gurobi_machines_plugin [-h] [-u [URL]] [-e [EXTRA_ARGS]] 
                                    [--client_id [CLIENT_ID]]
                                    [--client_secret [CLIENT_SECRET]]
                                    [--outdated_minutes [OUTDATED_MINUTES]]

        optional arguments:
                            -h, --help            show this help message and exit
                            -u [URL], --url [URL]
                                                    url to check
                            -e [EXTRA_ARGS], --extra_args [EXTRA_ARGS]
                                                    extra args to add to curl, see curl manpage
                            --client_id [CLIENT_ID]
                                                    Header client_id
                            --client_secret [CLIENT_SECRET]
                                                    Header client_secret
                            --outdated_minutes [OUTDATED_MINUTES]
                                                    Minutes to consider outdated

Example usage
=============

Example basic usage::

    > gurobi_machines_plugin --url 'https://cloud.gurobi.com/api/v2/pools/{PoolID}/machines' 
                             --client_id '{client_id}' --client_secret '{client_secret}' --outdated_minute 60

Nagios config
=============

Example command::

    define command{
        command_name  check_gurobi_machines
        command_line  /usr/local/bin/gurobi_machines_plugin --url '$ARG1$' --client_id '$ARG2$' --client_secret '$ARG3$' --outdated_minute $ARG4$  $ARG5$
    }

With proxy defined

# use gurobi_machines with proxy
define command{
    command_name  check_gurobi_machines_proxy
    command_line  https_proxy=http://user:pass@PROXYIP:PORT /usr/local/bin/gurobi_machines_plugin --url '$ARG1$' --client_id '$ARG2$' --client_secret '$ARG3$' --outdated_minute $ARG4$  $ARG5$
}

Example service::

    define service {
            host_name                       SERVERX
            service_description             service_name
            check_command                   check_gurobi_machines!https://cloud.gurobi.com/api/v2/pools/{PoolID}/machines!{client_id}!{client_secret}!60
            use				                generic-service
            notes                           some useful notes
    }
    
With proxy defined:

    define service {
            host_name                       SERVERX
            service_description             service_name
            check_command                   check_gurobi_machines_proxy!https://cloud.gurobi.com/api/v2/pools/{PoolID}/machines!{client_id}!{client_secret}!60
            use				                generic-service
            notes                           some useful notes
    }

You can use ansible role that already has the installation and command: https://github.com/CoffeeITWorks/ansible_nagios4_server_plugins

TODO
====

* Use hash passwords
* Add Unit tests?
