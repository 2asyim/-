from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QRadioButton, QButtonGroup, QComboBox,
    QPushButton, QLabel, QGroupBox, QTabWidget
)
from ui.delivery_tab import DeliveryAccountManager
from ui.document_tab import DocumentManager
from ui.client_list import ClientListManager
from utils.formatters import TextFormatters
from PyQt5.QtCore import Qt

class ClientManagerWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.formatters = TextFormatters()

        # 기본 설정
        self.setWindowTitle("거래처 정보 관리 프로그램")
        self.setGeometry(100, 100, 1100, 800)

        # UI 초기화
        self.setup_ui()

    def setup_ui(self):
        """전체 UI 설정"""
        self.tab_widget = QTabWidget()

        self.setup_client_tab()
        self.setup_vat_tab()
        self.setup_income_tax_tab()

        self.setCentralWidget(self.tab_widget)

    def setup_client_tab(self):
        """거래처 관리 탭 설정"""
        client_tab = QWidget()
        main_layout = QVBoxLayout()

        # 서브탭 생성
        self.sub_tab_widget = QTabWidget()

        # 기본정보 입력 서브탭
        self.setup_input_form()
        basic_info_tab = QWidget()
        basic_layout = QVBoxLayout()
        basic_layout.addLayout(self.top_layout)
        basic_layout.addWidget(self.bottom_widget)
        basic_info_tab.setLayout(basic_layout)
        self.sub_tab_widget.addTab(basic_info_tab, "기본정보 입력")

        # 배달계정 관리 서브탭
        self.delivery_manager = DeliveryAccountManager(self)
        delivery_tab = QWidget()
        delivery_layout = QVBoxLayout()
        delivery_layout.addWidget(self.delivery_manager.delivery_box)
        delivery_tab.setLayout(delivery_layout)
        self.sub_tab_widget.addTab(delivery_tab, "배달계정 관리")

        # 기본서류 첨부 서브탭
        self.document_manager = DocumentManager(self)
        document_tab = QWidget()
        document_layout = QVBoxLayout()
        document_layout.addWidget(self.document_manager.doc_box)
        document_tab.setLayout(document_layout)
        self.sub_tab_widget.addTab(document_tab, "기본서류 첨부")

        main_layout.addWidget(self.sub_tab_widget)

        client_tab.setLayout(main_layout)
        self.tab_widget.addTab(client_tab, "거래처 관리")

    def setup_input_form(self):
        """기본정보 입력폼 + 메모 + 검색/버튼 구성"""
        self.name_input = QLineEdit()
        self.biznum_input = QLineEdit()
        self.rep_input = QLineEdit()
        self.rrn_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.fee_input = QLineEdit()
        self.hometax_id_input = QLineEdit()
        self.hometax_pw_input = QLineEdit()

        self.ind_radio = QRadioButton("개인")
        self.corp_radio = QRadioButton("법인")
        self.biz_type_group = QButtonGroup()
        self.biz_type_group.addButton(self.ind_radio)
        self.biz_type_group.addButton(self.corp_radio)

        self.tax_type_combo = QComboBox()
        self.tax_type_combo.addItems(["일반", "간이", "면세"])

        self.memo_input = QTextEdit()

        # 좌측 입력폼 (1열)
        left_form = QFormLayout()
        left_form.addRow("상호명", self.name_input)
        left_form.addRow("사업자번호", self.biznum_input)
        left_form.addRow("대표자", self.rep_input)
        left_form.addRow("주민등록번호", self.rrn_input)
        left_form.addRow("연락처", self.phone_input)

        # 우측 입력폼 (2열)
        right_form = QFormLayout()
        right_form.addRow("기장료", self.fee_input)
        right_form.addRow("홈택스 ID", self.hometax_id_input)
        right_form.addRow("홈택스 PW", self.hometax_pw_input)

        biz_type_layout = QHBoxLayout()
        biz_type_layout.addWidget(self.ind_radio)
        biz_type_layout.addWidget(self.corp_radio)
        biz_type_widget = QWidget()
        biz_type_widget.setLayout(biz_type_layout)

        right_form.addRow("사업자 구분", biz_type_widget)
        right_form.addRow("세유형", self.tax_type_combo)

        # 상단 레이아웃
        form_layout = QHBoxLayout()
        form_layout.addLayout(left_form)
        form_layout.addLayout(right_form)

        memo_box = QGroupBox("메모")
        memo_layout = QVBoxLayout()
        memo_layout.addWidget(self.memo_input)
        memo_box.setLayout(memo_layout)

        self.top_layout = QHBoxLayout()
        self.top_layout.addLayout(form_layout, 2)
        self.top_layout.addWidget(memo_box, 1)

        # 검색창 + 버튼
        self.search_input = QLineEdit()
        self.search_button = QPushButton("검색")
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # 저장/수정/삭제 버튼
        self.save_button = QPushButton("저장")
        self.update_button = QPushButton("수정")
        self.delete_button = QPushButton("삭제")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        # 거래처 리스트
        self.client_list_manager = ClientListManager(self, self.database)
        self.client_list_manager.set_callback(self.load_client_data)

        # 하단 위젯 정리
        self.bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_layout.addLayout(search_layout)
        bottom_layout.addWidget(self.client_list_manager.widget)
        bottom_layout.addLayout(button_layout)
        self.bottom_widget.setLayout(bottom_layout)

    def setup_vat_tab(self):
        """부가세 신고 리스트 탭 설정"""
        self.vat_tab = QWidget()
        vat_layout = QVBoxLayout()
        vat_layout.addWidget(QLabel("🧾 부가세 신고 리스트 (준비 중)"))
        self.vat_tab.setLayout(vat_layout)
        self.tab_widget.addTab(self.vat_tab, "부가세 신고 리스트")

    def setup_income_tax_tab(self):
        """종합소득세 신고 리스트 탭 설정"""
        self.income_tab = QWidget()
        income_layout = QVBoxLayout()
        income_layout.addWidget(QLabel("🧾 종합소득세 신고 리스트 (준비 중)"))
        self.income_tab.setLayout(income_layout)
        self.tab_widget.addTab(self.income_tab, "종합소득세 신고 리스트")

    def load_client_data(self, client_name):
        """검색된 거래처 데이터 로드 (구현 예정)"""
        pass
