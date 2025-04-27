from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem
)

class ClientListManager:
    def __init__(self, parent=None, database=None):
        self.parent = parent
        self.database = database
        self.client_table = None
        self.on_client_clicked = None  # 거래처 선택 시 콜백 함수
        self.setup_ui()
        
    def setup_ui(self):
        """거래처 목록 UI 설정"""
        self.widget = QWidget()
        layout = QVBoxLayout()
        
        # 저장된 거래처 목록 라벨 추가
        layout.addWidget(QLabel("📋 저장된 거래처 목록"))

        # 거래처 목록 테이블 생성
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(3)  # 3개의 열 (상호, 대표자, 연락처)
        self.client_table.setHorizontalHeaderLabels(["상호", "대표자", "연락처"])
        self.client_table.cellClicked.connect(self.client_clicked)

        # 거래처 목록 테이블 추가
        layout.addWidget(self.client_table)
        self.widget.setLayout(layout)
        
    def load_all_clients(self):
        """모든 거래처 불러오기"""
        if not self.database:
            return
            
        # 테이블 초기화
        self.client_table.setRowCount(0)
        
        # DB에서 거래처 목록 조회
        clients = self.database.get_all_clients()
        
        # 테이블에 거래처 데이터 표시
        for row_index, (cid, name, rep, phone) in enumerate(clients):
            self.client_table.insertRow(row_index)
            self.client_table.setItem(row_index, 0, QTableWidgetItem(name))
            self.client_table.setItem(row_index, 1, QTableWidgetItem(rep))
            self.client_table.setItem(row_index, 2, QTableWidgetItem(phone))
            self.client_table.setRowHeight(row_index, 20)
            
    def client_clicked(self, row, column):
        """거래처 선택 시 이벤트 처리"""
        if self.on_client_clicked and row >= 0:
            client_name = self.client_table.item(row, 0).text()
            self.on_client_clicked(client_name)
            
    def set_callback(self, callback):
        """거래처 선택 시 호출될 콜백 함수 설정"""
        self.on_client_clicked = callback