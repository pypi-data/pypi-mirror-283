"""
Nova 프로젝트와 유사한 원격 디버깅 옵션을 지원하기 위한 코드

Ref: <https://opendev.org/openstack/nova/src/commit/8e4a7290f8467f1e915f3bb494ce61ade5aa511c/nova/conf/remote_debug.py>
"""
from oslo_config import cfg

debugger_group = cfg.OptGroup('remote_debug', title='debugger options')

ALL_OPTS = [
    cfg.HostAddressOpt(
        'host',
        help="""
디버깅 클라이언트를 연결할 서버 IP 혹은 이름
"""),
    cfg.PortOpt('port',
        help="""
디버깅 클라이언트를 연결할 서버의 포트
"""),
    cfg.BoolOpt('wait_for_client',
        default=False,
        help="""
(선택옵션) 디버깅 클라이언트의 연결이 될 때까지 실행을 기다린다. 코드의 초기화 과정을 기다릴 때 유용
Ref: <https://github.com/microsoft/debugpy/wiki/Command-Line-Reference#--wait-for-client>
"""),
]


def register_opts(conf):
    """'remote_debug' 그룹 옵션을 구성에 등록"""
    conf.register_opts(ALL_OPTS, group=debugger_group)

def list_opts():
    """'remote_debug' 그룹 옵션 내용"""
    return {debugger_group: ALL_OPTS}

def enabled(conf):
    """oslo_config의 remote_debug 활성화 여부 검사"""
    return (conf.remote_debug.host and conf.remote_debug.port)
