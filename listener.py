import bottle

from github import Categorize

@bottle.route('/', method=['GET', 'POST'])
def index():
    return "Not Implemented"

@bottle.route('/pullreq', method=['GET', 'POST'])
def github_hook(param=None):
    import pdb; pdb.set_trace()
    # try:
    Categorize(bottle.request).categorize(check_for='pull_request')
    return 0
    # except Exception as error:
    #     print "Error Log:", str(error)
    #     return 1

bottle.debug(True)
bottle.run(host='0.0.0.0', port=8000, reloader=True)
