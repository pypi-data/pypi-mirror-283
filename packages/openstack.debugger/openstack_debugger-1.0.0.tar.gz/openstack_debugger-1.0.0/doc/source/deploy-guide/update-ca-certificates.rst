=======================================
  Openstack Debugger 배포시 인증서 등록
=======================================

인증서 뷰어, 세부정보, 내보내기

.. image:: ../_static/chrome_certificate_export.png
   :height: 400px
   :width: 1200px
   :alt: Certificate Export

.. code-block:: shell

   # 사설 인증서를 신뢰할 수 있는 인증서로 등록하는 절차
   cp gitlabix_gabia_io.crt /usr/local/share/ca-certificates/

   update-ca-certificates