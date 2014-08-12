
from github3 import login


class Authentication(object):
    def authenticate(self):
        with open('secret.txt', 'r') as fp:
            token = [line.strip() for line in fp.readlines() if line.strip()][0]

        login_ = login(token=token)
        return login_
