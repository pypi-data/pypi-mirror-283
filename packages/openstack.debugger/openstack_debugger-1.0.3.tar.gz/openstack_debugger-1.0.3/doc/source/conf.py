# conf.py

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# 프로젝트 정보
project = 'openstack.debugger'
author = 'nobody'
release = '0.1'

# Sphinx 확장 모듈
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

# 소스 파일의 확장자
source_suffix = '.rst'

# 마스터 문서
master_doc = 'index'

# 제외할 패턴
exclude_patterns = []

# HTML 출력 설정
html_theme = 'alabaster'
html_static_path = ['_static']

# todo 지시어를 포함할지 여부
todo_include_todos = True
