from PyQt5.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class DeliveryAccountManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.delivery_table = None
        self.delivery_name = None
        self.delivery_id = None
        self.delivery_pw = None
        self.setup_ui()
        
    def setup_ui(self):
        """배달계정 관리 UI 설정"""
        # 배달계정 관리 영역
        self.delivery_box = QGroupBox("배달계정 관리")
        delivery_layout = QVBoxLayout()

        # 입력 필드
        self.delivery_name = QLineEdit()
        self.delivery_name.setPlaceholderText("업체명")
        self.delivery_id = QLineEdit()
        self.delivery_id.setPlaceholderText("ID")
        self.delivery_pw = QLineEdit()
        self.delivery_pw.setPlaceholderText("PW")

        # 가로로 배치
        delivery_input_layout = QHBoxLayout()
        delivery_input_layout.addWidget(self.delivery_name)
        delivery_input_layout.addWidget(self.delivery_id)
        delivery_input_layout.addWidget(self.delivery_pw)

        # 버튼
        self.add_btn = QPushButton("추가")
        self.del_btn = QPushButton("삭제")
        self.add_btn.clicked.connect(self.add_delivery)
        self.del_btn.clicked.connect(self.remove_delivery)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.del_btn)

        # 테이블 (업체명, ID, PW)
        self.delivery_table = QTableWidget(0, 3)
        self.delivery_table.setHorizontalHeaderLabels(["업체명", "ID", "PW"])

        # 레이아웃에 배치
        delivery_layout.addLayout(delivery_input_layout)
        delivery_layout.addLayout(button_layout)
        delivery_layout.addWidget(self.delivery_table)
        self.delivery_box.setLayout(delivery_layout)

    def add_delivery(self):
        """배달계정 추가"""
        name = self.delivery_name.text().strip()
        did = self.delivery_id.text().strip()
        pw = self.delivery_pw.text().strip()
        
        if name and did and pw:  # 값이 있을 때만 추가
            row = self.delivery_table.rowCount()  # 현재 테이블의 행 수
            self.delivery_table.insertRow(row)  # 새로운 행 추가
            self.delivery_table.setItem(row, 0, QTableWidgetItem(name))  # 업체명 추가
            self.delivery_table.setItem(row, 1, QTableWidgetItem(did))  # ID 추가
            self.delivery_table.setItem(row, 2, QTableWidgetItem(pw))  # PW 추가
            
            # 입력창 초기화
            self.delivery_name.clear()
            self.delivery_id.clear()
            self.delivery_pw.clear()
        else:
            QMessageBox.warning(self.parent, "입력 오류", "모든 항목을 입력해주세요.")

    def remove_delivery(self):
        """배달계정 삭제"""
        selected = self.delivery_table.currentRow()  # 선택된 행
        if selected >= 0:  # 행이 선택되었을 때
            self.delivery_table.removeRow(selected)  # 선택된 행 삭제
        else:
            QMessageBox.warning(self.parent, "선택 오류", "삭제할 항목을 선택해주세요.")
            
    def get_all_accounts(self):
        """모든 배달계정 정보 반환"""
        accounts = []
        for row in range(self.delivery_table.rowCount()):
            account = {
                'company': self.delivery_table.item(row, 0).text(),
                'did': self.delivery_table.item(row, 1).text(),
                'dpw': self.delivery_table.item(row, 2).text()
            }
            accounts.append(account)
        return accounts
        
    def clear(self):
        """모든 배달계정 삭제"""
        self.delivery_table.setRowCount(0)
        self.delivery_name.clear()
        self.delivery_id.clear()
        self.delivery_pw.clear()