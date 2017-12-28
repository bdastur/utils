#!/usr/bin/env python
# -*- coding: utf-8 -*-

import src.pydashing_cli as dashingcli
import src.cfgparser as cfgparser

def main():
    cli = dashingcli.PyDashingCli()
    cfg_parser = cfgparser.PyDashingConfigParser(cli.cliobj['config_file'])
    print "Parsed data: ", cfg_parser.parsed_data

if __name__ == '__main__':
    main()
