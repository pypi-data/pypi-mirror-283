=================================
  Openstack Debugger 배포
=================================

PyPI 레지스트리에 배포하는 기능은 포함되어 있지 않기 때문에, 별도로 `twine` 라이브러리를 사용합니다.

.. code-block:: shell

   # PyPI 사설 레지스트리에 업로드 하기 위해, `twine` 설치
   pip install twine

   twine upload --repository-url https://openstack-repo.gabia.com/repository/pypi-local/ dist/* --username <your-username> --password <your-password>

.. toctree::
   :maxdepth: 3

   update-ca-certificates