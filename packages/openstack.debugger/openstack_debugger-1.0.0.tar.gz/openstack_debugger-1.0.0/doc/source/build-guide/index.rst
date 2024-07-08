==================================
  Openstack Debugger 프로젝트 빌드
==================================

.. code-block:: shell

   # 프로젝트 빌드
   pip install -e .

   # 소스(dist/*.tar.gz), 바이너리(dist/*.whl) 패키징 (Git Tag 버전 인용)
   python setup.py sdist bdist_wheel
