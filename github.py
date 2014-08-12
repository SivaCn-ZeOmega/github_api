
try:
    import simplejson as json
except:
    import json

from Handler import ArgumentError, NotValidRequest, EmptyRequestBodyError
from Handler import NotHookedForPullRequest
from secure import Authentication


class HelperMethods(object):
    def __init__(self, context):
        self.context = context

    def read_json_data(self):
        if not self.context:
            raise NotValidRequest("Not a Valid Request Object")

        if not self.context.body.read().strip():
            raise EmptyRequestBodyError("Request body is Empty while read")

        return json.loads(self.context.body.read())

    def get_any_data_from_payload(self, payload, reference_template):
        _stmt_as_str = ["['{0}']".format(ele) for ele in reference_template]
        _data = 'payload{0}'.format(''.join(_stmt_as_str).strip())

        return eval(_data)


class PullRequest(Authentication, HelperMethods):
    def __init__(self, context):
        super(PullRequest, self).__init__(context)
        self.context = context

        self.mstr_repo_templ = ('pull_request', 'base', 'label')
        self.forked_repo_reference_templ = ('pull_request', 'base', 'ref')

    def validate(self):
        """Validate weather it's a valid Event(pull_request)."""
        _data = self.read_json_data()
        if 'pull_request' in _data:
            return _data
        return False

    def __call__(self):

        _payload = self.validate()

        if not _payload:
            raise NotHookedForPullRequest("Not a valid Web-Hook for Pull Request")

        import pdb; pdb.set_trace()

        # Find the Master and Slave Repos
        # where Master --> base/origin repo
        # and forked --> a clone of a Master repo.
        master_repo = self.get_any_data_from_payload(_payload, self.mstr_repo_templ)
        slave_repo = self.get_any_data_from_payload(_payload, self.forked_repo_reference_templ)

        # find the branches of Master and Forked Repos.
        master_branch = self.get_any_data_from_payload(_payload, self.mstr_repo_templ)
        forked_branch = self.get_any_data_from_payload(_payload, self.forked_repo_reference_templ)

        # Authenticate user from GitHub
        github = self.authenticate()


class Categorize(object):
    def __init__(self, context):
        self.context = context

        self.mapper = {
            'pull_request': PullRequest
        }

    def categorize(self, check_for=None):
        # check for specific Attributes.
        if check_for is None:
            raise ArgumentError("Argument 'check_for' cannot be None type or empty")

        if check_for not in self.mapper:
            raise NotImplementedError("Feature Not Implemented for {0}".format(check_for))

        # Return an Callable object of the Attributes.
        category_object = self.mapper[check_for](self.context)
        return category_object()
