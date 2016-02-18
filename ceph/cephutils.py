#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rados
import json
import pprint

conffile = "/etc/ceph/ceph.conf"


def main():
    print "main"
    try:
        cluster = rados.Rados(conffile=conffile)
        cluster.connect()

        cmd = {"prefix": "osd tree", "format": "json"}
        ret, buf, err = cluster.mon_command(json.dumps(cmd), "")
        print "%s, %s, %s" % (str(ret), buf, str(err))

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(json.loads(buf))

    except rados.Error as err:
        print "Failed to instantiate cluster [ %s ]" % err
        sys.exit(1)
    print "librados version: ", str(cluster.version())

if __name__ == '__main__':
    main()
