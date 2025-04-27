import sys
from PyQt5.QtWidgets import QApplication
from db.database import ClientDatabase
from ui.main_window import ClientManagerWindow

def main():
    # PyQt 애플리케이션 생성
    app = QApplication(sys.argv)
    
    # 데이터베이스 초기화
    database = ClientDatabase()
    
    # 메인 윈도우 생성
    window = ClientManagerWindow(database)
    
    # 윈도우 표시
    window.show()
    
    # 애플리케이션 실행
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()