from PyQt5.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QPushButton, QLabel, QWidget, QFileDialog
)
from datetime import datetime

class DocumentManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.doc_labels = []
        self.doc_names = ["사업자등록증", "통장사본", "임대차계약서", "신분증", "차량등록증"]
        self.setup_ui()
        
    def setup_ui(self):
        """기본서류 첨부 UI 설정"""
        # 기본서류 첨부 영역 생성
        self.doc_box = QGroupBox("기본서류 첨부")
        doc_layout = QFormLayout()

        # 서류마다 첨부 버튼과 라벨 추가
        for name in self.doc_names:
            btn = QPushButton(f"{name} 첨부")
            label = QLabel("미첨부")
            
            # 버튼 클릭 시 파일 첨부 함수 호출
            btn.clicked.connect(lambda _, l=label: self.attach_file(l))
            
            row = QHBoxLayout()
            row.addWidget(btn)
            row.addWidget(label)
            container = QWidget()
            container.setLayout(row)
            doc_layout.addRow(name, container)
            self.doc_labels.append(label)

        # 레이아웃 설정
        self.doc_box.setLayout(doc_layout)

    def attach_file(self, label):
        """파일 첨부 기능"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 
            "파일 선택", 
            "", 
            "All Files (*);;PDF Files (*.pdf);;Image Files (*.png *.jpg *.bmp)"
        )

        if file_path:
            # 파일이 선택되면, 첨부된 시간 추가
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            label.setText(f"첨부됨: {timestamp}")
            
    def get_documents(self):
        """모든 첨부 서류 정보 반환"""
        documents = []
        for i, label in enumerate(self.doc_labels):
            uploaded_time = None
            if "첨부됨" in label.text():
                uploaded_time = label.text().replace("첨부됨: ", "")
                
            doc = {
                'name': self.doc_names[i],
                'uploaded_time': uploaded_time
            }
            documents.append(doc)
        return documents
        
    def clear(self):
        """모든 첨부 서류 정보 초기화"""
        for label in self.doc_labels:
            label.setText("미첨부")