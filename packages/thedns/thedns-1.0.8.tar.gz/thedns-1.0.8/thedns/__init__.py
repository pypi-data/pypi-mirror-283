import requests
import pathlib
from .auth import _token
from .auth import _credentials
from .auth import _request_headers
from .network import _get_private_ip
from .network import _get_rr_string
from .wanwang import _list_rrs
from .wanwang import _build_payload
from .wanwang import _update_rr

class DDNS(object):
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
        self.system_uuid = _get_rr_string()
        self.rr_string_public = self.system_uuid + '.public'
        self.rr_string_private = self.system_uuid + '.private'
    def update(self):
        _update_rr(request_headers=self.request_headers, rr_record=self.rr_string_private,rr_value=self.private_ip)
        _update_rr(request_headers=self.request_headers, rr_record=self.rr_string_public,rr_value=self.public_ip)
        config_dir = pathlib.Path.home() / '.devnull'
        pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
        fqdn_file = config_dir / 'fqdn'
        with fqdn_file.open('wt') as f:
            f.write('\n'.join([self.system_uuid, self.rr_string_public, self.rr_string_private]))
        return {
            self.rr_string_public + '.thedns.cn': self.public_ip,
            self.rr_string_private + '.thedns.cn': self.private_ip,
            'fqdn': fqdn_file.as_posix(),
        }
