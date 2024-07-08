==================================================
OpenStack 프로젝트에서 디버거를 활성화 시키는 방법
==================================================

먼저, 서비스 애플리케이션의 oslo_config로 쓸 수 있도록 구성 파일을 읽어들여야 한다.

    구성 파일에는 `[remote_debug]` 섹션을 정의할 수 있다.

    .. code-block:: ini

        [remote_debug]
        host = 0.0.0.0 # 디버깅 클라이언트를 연결할 서버 IP 혹은 이름
        port = 5678 # 디버깅 클라이언트를 연결할 서버의 포트
        wait_for_client = False # (선택옵션) 디버깅 클라이언트의 연결이 될 때까지 실행을 기다린다. 코드의 초기화 과정을 기다릴 때 유용 (기본값: False)

remote_debug 모듈을 통해, oslo_config 객체에 설정값을 등록하고, 설정 정보가 있는 경우에는 디버거를 초기화 시킨다.

.. code-block:: python

    from openstack_debugger.conf import remote_debug
    remote_debug.register_opts(CONF) # CONF: <oslo_config.cfg.CONF> 객체

    if (CONF.remote_debug.host and CONF.remote_debug.port):
        from openstack_debugger import debugger
        debugger.init()
