"""
Nova 프로젝트와 유사한 원격 디버깅 옵션을 지원하기 위한 코드

Ref: <https://opendev.org/openstack/nova/src/commit/8e4a7290f8467f1e915f3bb494ce61ade5aa511c/nova/debugger.py>
"""
from oslo_log import log as logging
import debugpy
from oslo_config import cfg

def init():
    """원격 디버거 초기화"""
    CONF = cfg.CONF

    if 'remote_debug' not in CONF:
        return

    if not (CONF.remote_debug.host and CONF.remote_debug.port):
        return

    LOG = logging.getLogger(__name__)

    LOG.debug('Listening on %(host)s:%(port)s for debug connection',
              {'host': CONF.remote_debug.host,
               'port': CONF.remote_debug.port})

    debugpy.listen((CONF.remote_debug.host, CONF.remote_debug.port))

    if CONF.remote_debug.wait_for_client:
        debugpy.wait_for_client()
