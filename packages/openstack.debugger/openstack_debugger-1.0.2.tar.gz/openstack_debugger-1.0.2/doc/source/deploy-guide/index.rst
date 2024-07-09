=================================
  Openstack Debugger 배포
=================================

.. code-block:: shell

   # 소스(dist/*.tar.gz), 바이너리(dist/*.whl) 패키징 (Git Tag 버전 인용)
   python setup.py sdist bdist_wheel

   # PyPI 레지스트리에 배포하는 기능은 포함되어 있지 않기 때문에, 별도로 `twine` 설치가 필요
   pip install twine

   # PyPI 사설 레지스트리(openstack-repo.gabia.io)에 업로드 하기 위해, `twine` 설치
   # NOTE: "~/.pypirc"로 alias 지정 가능 <https://packaging.python.org/en/latest/specifications/pypirc/>
   # FIXME: 제대로 동작하지 않는 경우가 발생하므로, http('s' 빼고)로 변경하여 시도
   twine upload --repository-url https://openstack-repo.gabia.com/repository/pypi-local/ dist/* --username <your-username> --password <your-password>

.. toctree::
   :maxdepth: 3

   update-ca-certificates