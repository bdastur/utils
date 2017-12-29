#!/usr/bin/env python
# -*- coding: utf-8 -*-

import src.pydashing_cli as dashingcli
import src.cfgparser as cfgparser
import src.pydashing_renderer as renderer

def main():
    cli = dashingcli.PyDashingCli()
    cfg_parser = cfgparser.PyDashingConfigParser(cli.cliobj['config_file'])
    print "Parsed data: ", cfg_parser.parsed_data
    dashing_renderer = renderer.PyDashingRenderer(
        cfg_parser.parsed_data,
        cli.cliobj['render_path'],
        dashboard_templates="../dashboard_templates")

if __name__ == '__main__':
    main()
