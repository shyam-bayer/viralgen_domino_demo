'''

Boilerplate script for new Dash applications.

Original author: John Mason
Date: May 2021

This script is meant to serve as a starting place for developing a Dash 
application.  Features:
- Fixes Dash URLs for launching in a Domino workspace or deploying on Domino.
- Imports for the basic (and some advanced) components libraries.
- Imports and setup for on-disk caching of intermediates.  This code is disabled
    by default.

I recommend running any application via a Flask debugger configuration in VS 
Code.  This script should be distributed with a proper launch configuration.

'''

import sys
import os
import argparse

import dash
import dash.dependencies as dd # for .Input, .Output, .State
import dash_core_components as dcc # Basic input/output, figures
import dash_html_components as html # Standard HTML tags
import dash_bootstrap_components as dbc # Layout, advanced widgets and styling
# import dash_table # Advanced table component (.DataTable)
# See Dash documentation for other component libraries

import plotly.express as px # High-level plotting
import plotly.graph_objects as go # Low-level plotting

# from flask_caching import Cache # For on-disk caching

try:
    # These arguments are added when launching the Flask debugger, but for some
    # reason aren't removed from the arguments before launching the Python 
    # application.
    sys.argv.remove('run')
    sys.argv.remove('--no-debugger')

except ValueError:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('--deploy', action = 'store_true')

args = parser.parse_args()

if args.deploy:
    # See https://docs.dominodatalab.com/en/4.2/reference/publish/apps/Getting_started_with_Dash.html
    HOST = '0.0.0.0'
    PORT = '8888'

    REQUESTS_PREFIX = '/'.join([
        '',
        '{DOMINO_PROJECT_OWNER}',
        '{DOMINO_PROJECT_NAME}',
        'r',
        'notebookSession',
        '{DOMINO_RUN_ID}',
        ''
    ]).format(**os.environ)

else:
    HOST = '127.0.0.1' # Default for Dash applications
    PORT = '5000' # Default for Flask debugging

    REQUESTS_PREFIX = '/'.join([
        '',
        '{DOMINO_STARTING_USERNAME}', # might need to be DOMINO_PROJECT_OWNER
        '{DOMINO_PROJECT_NAME}',
        'notebookSession',
        '{DOMINO_RUN_ID}',
        'proxy',
        str(PORT),
        ''
    ]).format(**os.environ)
    print(f'Open https://domino.sats.cloud{REQUESTS_PREFIX} in your browser')

app = dash.Dash(
    __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP],
    requests_pathname_prefix = REQUESTS_PREFIX
)
application = app.server

# cache = Cache( # Bind to function with @cache.memoize(timeout = <seconds>)
#     application,
#     config = {
#         'CACHE_TYPE': 'FileSystemCache',
#         'CACHE_DIR': 'flask-cache'
#     }
# )

# Application code goes here

app.layout = dbc.Container(
    'Hello world'
)

if __name__ == '__main__':
    app.run_server(debug = False, port = PORT, host = HOST)
