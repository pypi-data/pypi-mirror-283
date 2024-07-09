import requests
import pathlib
import base64
from .auth import _token
from .auth import _credentials
from .auth import _request_headers
from .utils import _get_private_ip
from .utils import _get_fqdn_id
from .utils import _create_ca
from .utils import _create_cert
from .utils import _get_ca
from .utils import _get_certs

class CA(object):
    access_key = None
    secret_key = None
    email = None
    public_ip = None
    private_ip = None
    token = None
    request_headers = None
    def __init__(self):
        self.access_key, self.secret_key, self.email = _credentials()
        self.public_ip = requests.get('https://devnull.cn/ip').json()['origin']
        self.private_ip = _get_private_ip()
        self.token = _token(self.email, self.access_key, self.secret_key)
        self.request_headers = _request_headers(token=self.token)
        self.system_uuid = _get_fqdn_id()
        self.common_names = [ self.system_uuid, self.system_uuid + '.private.thedns.cn', self.system_uuid + '.public.thedns.cn']
    def get_ca(self):
        return _get_ca(request_headers=self.request_headers)
    def get_certs(self):
        return _get_certs(request_headers=self.request_headers)
    def create_ca(self):
        return _create_ca(request_headers=self.request_headers)
    def create_cert(self):
        # return _create_cert(request_headers=self.request_headers,common_names=self.common_names)
        data =  _create_cert(request_headers=self.request_headers,common_names=self.common_names)
        common_name = self.common_names[0]
        config_dir = pathlib.Path.home() / '.devnull' / 'certs' / common_name
        pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
        key_file = config_dir / 'key.pem'
        crt_file = config_dir / 'crt.pem'
        chain_file = config_dir / 'fullchain.pem'
        ca_file = config_dir / 'ca.pem'
        key_string_b64 = data['key']
        crt_string_b64 = data['crt']
        ca_string_b64 = data['ca']
        key_string = base64.b64decode(key_string_b64).decode()
        crt_string = base64.b64decode(crt_string_b64).decode()
        ca_string = base64.b64decode(ca_string_b64).decode()
        with crt_file.open('wt') as f:
            f.write(crt_string)
        with key_file.open('wt') as f:
            f.write(key_string)
        with chain_file.open('wt') as f:
            f.write(crt_string + '\n' + ca_string)
        with ca_file.open('wt') as f:
            f.write(ca_string)
        return {
            'key': key_file,
            'crt': crt_file,
            'full_chain': chain_file,
            'ca': ca_file,
            'reminder': 'You need add CA into your trusted authorities.'
        }

"""
import theca; ca = theca.CA(); ca.get_ca()


"""