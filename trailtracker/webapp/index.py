#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, Response, session
import json
import time
import multiprocessing
import main.trailtracker as trailtracker


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cloudtraillogging'


def iter_all_rows():
    rows = ["this, is, a, test",
    "this, is, a, test",
    "this, is, a, test",
    "this, is, a, test",
    "this, is, a, test",
    "this, is, a, test",]
    return rows

@app.route('/largecsv')
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')


def stream_template(template_name, **context):
    print "Stream template"
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


@app.route('/page1')
def render_large_template():
    rows = iter_all_rows()
    return Response(stream_template('sample.html', rows=rows))

common_obj = None
done = False
app_queue = None

def listener_callback(objdata, app_queue):
    with app.test_request_context():
        global common_obj
        global done

        if objdata.get('done', None) is not None:
            print "SET Done to True"
            common_obj = None
            done = True
        else:
            print "SET COMMON OBJ and session"
            common_obj = objdata
            session['common_obj'] = objdata
            app_queue.put(objdata)
        print "COMMON OBJECT: ", common_obj


def gen(session):
    while True:
        try:
            objdata = app_queue.get(timeout=3)
        except multiprocessing.queues.Empty:
            continue

        if objdata is None:
            continue

        print "OBJDATA in GEN: ", objdata
        objdata['eventTime'] = \
            objdata['eventTime'].strftime('%Y/%m/%d:%H:%M:%S')

        try:
            yield json.dumps(objdata)
        except TypeError:
            print "objdata: %s is not json serializable" % objdata


def oldgen(session):
    with app.test_request_context():
        print "GEN START>>>>>>> "
        global common_obj
        while True:
            print "common obj: ", common_obj
            if done:
                print "Generator Done........."
                break

            if session.get('common_obj', None) is None:
                print "session object is none"
                time.sleep(1)
                continue

            print "session obj: ", session['common_obj']

            # if common_obj is None:
            #     time.sleep(1)
            #     continue

            yield json.dumps(session['common_obj'])


def stream_trail_template(template_name, **context):
    print "Stream template"
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

def start_trail_search(myargs):
    profile_name = os.environ.get('TT_PROFILE_NAME', None)
    bucket_name = os.environ.get('TT_BUCKET_NAME', None)
    ttracker = trailtracker.TrailTracker(profile_name,
                                         bucket_name)

    ttracker.search_trail_archives(**myargs)
    #return Response(stream_trail_template('sample.html', **myargs))

@app.route('/page2')
def render_trail_records():
    session['common_obj'] = None
    myargs = {}
    myargs['accountname'] = "cpedevtest"
    myargs['region'] = "us-east-1"
    myargs['year'] = 2016
    myargs['months'] = [12]
    myargs['days'] = [29]

    global app_queue
    app_queue = multiprocessing.Queue()

    myargs['custom_callback'] = listener_callback
    myargs['custom_callback_args'] = app_queue
    search_args = {}
    search_args['eventName'] = "RunInstance"
    myargs['search_args'] = search_args
    worker = multiprocessing.Process(target=start_trail_search,
                                      args=(myargs,))
    worker.start()
    return Response(gen(session),content_type='text/event-stream')
    worker.join()

    #return Response(stream_trail_template('sample.html', **myargs))
    #return Response(gen(),content_type='text/event-stream')



@app.route("/")
def index():
    print "Index invoked..."
    return "Hello"

def main():
    app.run(host="127.0.0.1", port=5001, debug=True)

if __name__ == '__main__':
    main()
