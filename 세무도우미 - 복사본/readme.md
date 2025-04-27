client_manager/
│
├── main.py                 # 프로그램 시작점
├── db/
│   ├── __init__.py
│   └── database.py         # 데이터베이스 관련 기능
│
├── ui/  # UI 관련 모듈
│   ├── __init__.py
│   ├── main_window.py      # 메인 창 클래스
│   ├── delivery_tab.py     # 배달계정 관련 UI
│   ├── document_tab.py     # 서류 첨부 관련 UI
│   └── client_list.py      # 거래처 목록 관련 UI
│
└── utils/  # 유틸리티 모듈
    ├── __init__.py
    └── formatters.py       # 텍스트 포맷팅 유틸리티