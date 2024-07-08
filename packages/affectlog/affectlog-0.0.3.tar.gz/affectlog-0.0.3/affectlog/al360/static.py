import json
import webbrowser
import random
import socket
import logging
import sys
from .server import convert

def try_port(port):
    """Tests if port is available

    Parameters
    -----------
    port : int
        Port number

    Returns
    --------
    bool
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("127.0.0.1", port))
        result = True
    except:
        pass
    sock.close()
    return result

def get_free_port(n=10):
    """Generate random ports and return the first available

    Parameters
    -----------
    n : int
        Number of tries

    Returns
    --------
    int or None
    """
    for i in range(n):
        port = random.randrange(1024, 49152)
        if try_port(port):
            return port
    return None

def start_authorization_server(host, port):
    """Function starts server to cach OAuth redirect

    Server has one endpoint /. If it is called with token in query
    then server is closed and this function returns that token.

    Parameters
    -----------
    host : str
        Host address
    port : int
        Port number

    Returns
    --------
    str
    """
    from flask import Flask, request, abort, Response
    from flask_cors import CORS

    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None
    app = Flask(__name__)
    CORS(app)
    
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True

    result = {}

    @app.route("/", methods=['GET'])
    def main():
        token = request.args.get('token')
        if token is None:
            abort(404)
        result['token'] = token
        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown is None:
            raise Exception('Failed to stop the authorization server.')
        shutdown()
        return '<script>window.close()</script>'

    app.run(host=host, port=port)
    return result.get('token')

def get_json(al360):
    """Generate static AL360 data source in JSON format

    Function run calculations for all not cached plots. Then all
    are exported as static data source JSON.

    Parameters
    -----------
    al360 : object of class AL360
        AL360 object

    Returns
    --------
    str
    """
    al360.plots_manager.fill_cache()
    result = json.dumps({
        'version': '1.2.0',
        'availableParams': al360.list_available_params(),
        'paramsAttributes': al360.get_params_attributes(),
        'data': list(map(lambda p: p.serialize(), al360.plots_manager.cache))
    }, default=convert)
    return result

def generate_token():
    """Starts OAuth authorization and returns token

    Returns
    --------
    str
    """
    import requests
    client_id = 'd7d96eec80f68c16954b'
    uuid = str(random.randrange(2<<63))
    port = get_free_port()
    if port is None:
        raise Exception('Cannot find available port to start authorization server.')
    redirect = 'https://affectlog.com/al360/?connector=' + str(port)
    webbrowser.open('https://github.com/login/oauth/authorize?client_id=' + client_id + '&state=' + uuid + '&scope=gist&redirect_uri=' + redirect)
    return start_authorization_server('127.0.0.1', port)

def upload_al360(al360, token):
    """Uploads AL360 to GitHub Gist

    Function run calculations for all not cached plots. Then all
    are exported as static data source and uploaded to GitHub Gist.

    Parameters
    -----------
    al360 : object of class AL360
        AL360 object
    token : str
        GitHub access token

    Returns
    --------
    Link to uploaded data source
    """
    import requests
    json_str = get_json(al360)
    req = requests.post('https://api.github.com/gists', data=json.dumps({
        'public': False,
        'description': 'AL360 static data source',
        'files': { 'datasource.json': { 'content': json_str } }
    }), headers={
        'Authorization': 'token ' + token
    })
    if not req.ok:
        raise Exception('Failed to upload AL360')
    try:
        url = req.json().get('files').get('datasource.json').get('raw_url')
    except:
        raise Exception('GitHub returned invalid response')
    return url
