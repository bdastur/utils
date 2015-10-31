#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Openstack configuration aggregator.
"""

import yaml
import paramiko
import scp
import os
import argparse
import datetime


class FileHandler(object):
    '''
    Class that handles reading the setup file
    '''
    def __init__(self, filename="./setup.yaml"):
        '''
        Initialize class
        '''

        self.yamlfile = filename
        self.parsed = None
        try:
            fhandle = open(self.yamlfile)
        except IOError:
            print "Failed to read %s" % self.yamlfile
            return
        try:
            self.parsed = yaml.safe_load(fhandle)
        except yaml.parser.ParserError as parse_err:
            print "Failed to parse %s [%s]" % (self.yamlfile, parse_err)
            return

        print "Successfully initialized Filehandle"

    def get_parsed_data(self, keys):
        '''
        Given a key, get the parsed data
        '''
        if not isinstance(keys, list):
            print "Expected a list of keys"
            msg = """Example:
                Given a yaml construct as below:
                    SERVERS:
                        server1:
                            ssh_ip: "1.1.1.1"
                If looking for ssh_ip of server1, then the keylist would
                be ["SERVERS", "server1", "ssh_ip"]
                """
            print msg
            return None

        parsed = self.parsed
        for key in keys:
            parsed = parsed.get(key)

        return parsed

    def get_server_ssh_ips(self, role=None):
        '''
        Return the server ssh ip addresses as a list.
        '''
        serverip_list = []
        servers = self.get_parsed_data(["SERVERS"])
        for server in servers:
            serverip_list.append(server['ssh_ip'])

        return serverip_list

    def get_server_list(self, role=None):
        '''
        Return the server list
        '''
        return self.get_parsed_data(["SERVERS"])

    def get_server_username(self, server):
        '''
        Get the username for the server to login.
        '''
        username = None
        try:
            username = server['username']
        except KeyError:
            username = self.get_parsed_data(["USERNAME"])

        return username

    def get_server_password(self, server):
        '''
        Get the password for the server to login.
        '''
        password = None
        try:
            password = server['password']
        except KeyError:
            password = self.get_parsed_data(['PASSWORD'])

        return password


def create_local_path(filehandle,
                      server):
    '''
    Create local directory
    '''
    local_root = filehandle.get_parsed_data(["LOCAL_ROOT"])

    # Create local staging folder.
    if not os.path.exists(local_root):
        os.mkdir(local_root)

    svr_path = os.path.join(local_root, server['ssh_ip'])
    if not os.path.exists(svr_path):
        os.mkdir(svr_path)

    local_staging_folder = svr_path

    return local_staging_folder


def get_service_configuration(filehandle,
                              server,
                              sshclient):
    '''
    Generic service configuration generator
    '''
    service_list = filehandle.get_parsed_data(["SERVICES"])
    local_staging_folder = create_local_path(filehandle, server)

    print "service list: ", service_list, local_staging_folder
    for service in service_list:
        service_config_path = service.get('configpath')
        service_name = service.get('name')
        if service_config_path is None or service_name is None:
            print "Service config incorrect [%s]", service
            continue

        service_local_path = os.path.join(local_staging_folder, service_name)
        if os.path.exists(service_local_path):
            print "%s already present" % service_local_path
            curtime = datetime.datetime.now()
            timestamp = str(curtime.year) + str(curtime.month) + \
                str(curtime.day) + str(curtime.hour) + str(curtime.minute)
            service_name = service_name + "_" + timestamp
            service_local_path = os.path.join(
                local_staging_folder, service_name)

        scpclient = scp.SCPClient(sshclient.get_transport())
        scpclient.get(service_config_path,
                      local_path=service_local_path,
                      recursive=True)


def create_ssh_connection(server, username, password):
    '''
    Create a SSH connection using paramiko module
    '''
    if not server or not username or not password:
        print "Invalid params. Required: server, username and password"
        return None

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(server, username=username, password=password)

    return client


def main():
    '''
    Main
    '''
    print "main:"
    parser = argparse.ArgumentParser(description="Config Aggregator")
    parser.add_argument("--file",
                        help="setup file (yaml format)",
                        required=False)
    args = parser.parse_args()
    if not args.file:
        print "Using default setup.yaml file."
        args.file = "./setup.yaml"

    print args.file

    filehandle = FileHandler(args.file)
    servers = filehandle.get_server_list()

    for server in servers:
        username = filehandle.get_server_username(server)
        password = filehandle.get_server_password(server)
        print "%s, %s, %s", server['ssh_ip'], username, password

        sshclient = create_ssh_connection(server['ssh_ip'],
                                          username,
                                          password)
        if not sshclient:
            print "cannot connect to %s " % server['ssh_ip']

        get_service_configuration(filehandle, server, sshclient)


if __name__ == '__main__':
    main()
