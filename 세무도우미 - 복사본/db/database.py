import sqlite3
import os
from datetime import datetime

class ClientDatabase:
    def __init__(self, db_path="client_data.db"):
        self.db_path = db_path
        self.init_db()
        
    def init_db(self):
        """데이터베이스 및 테이블 초기화"""
        # DB 연결
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # clients 테이블 생성
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            biznum TEXT,
            representative TEXT,
            rrn TEXT,
            phone TEXT,
            fee TEXT,
            tax_type TEXT,
            hometax_id TEXT,
            hometax_pw TEXT,
            memo TEXT
        )
        """)

        # delivery_accounts 테이블 생성
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS delivery_accounts (
            client_id INTEGER,
            company TEXT,
            did TEXT,
            dpw TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """)

        # documents 테이블 생성
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            client_id INTEGER,
            doc_name TEXT,
            uploaded_time TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """)

        # 변경사항 커밋하고 연결 종료
        conn.commit()
        conn.close()
        
    def save_client(self, client_data, delivery_accounts, documents):
        """거래처 정보 저장"""
        # DB 연결
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 트랜잭션 시작
            conn.execute("BEGIN")
            
            # clients 테이블에 거래처 정보 저장
            cursor.execute("""
            INSERT INTO clients (name, biznum, representative, rrn, phone, fee, tax_type, hometax_id, hometax_pw, memo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                client_data['name'], 
                client_data['biznum'], 
                client_data['representative'], 
                client_data['rrn'], 
                client_data['phone'], 
                client_data['fee'], 
                client_data['tax_type'], 
                client_data['hometax_id'], 
                client_data['hometax_pw'], 
                client_data['memo']
            ))
            
            # 저장된 거래처의 ID 가져오기
            client_id = cursor.lastrowid
            
            # 배달계정 정보 저장
            for account in delivery_accounts:
                cursor.execute("""
                INSERT INTO delivery_accounts (client_id, company, did, dpw)
                VALUES (?, ?, ?, ?)
                """, (client_id, account['company'], account['did'], account['dpw']))
                
            # 서류 첨부 정보 저장
            for doc in documents:
                if doc['uploaded_time']:
                    cursor.execute("""
                    INSERT INTO documents (client_id, doc_name, uploaded_time)
                    VALUES (?, ?, ?)
                    """, (client_id, doc['name'], doc['uploaded_time']))
                    
            # 트랜잭션 커밋
            conn.commit()
            return True, client_id
            
        except Exception as e:
            # 오류 발생 시 롤백
            conn.rollback()
            return False, str(e)
            
        finally:
            # 연결 종료
            conn.close()
            
    def get_all_clients(self):
        """모든 거래처 목록 조회"""
        if not os.path.exists(self.db_path):
            return []
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, representative, phone FROM clients ORDER BY id DESC")
        results = cursor.fetchall()
        
        conn.close()
        return results
        
    def get_client_by_name(self, name):
        """이름으로 거래처 상세 정보 조회"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 거래처 기본 정보 조회
        cursor.execute("SELECT * FROM clients WHERE name = ?", (name,))
        client_data = cursor.fetchone()
        
        result = None
        if client_data:
            # 배달계정 정보 조회
            cursor.execute("SELECT company, did, dpw FROM delivery_accounts WHERE client_id = ?", (client_data[0],))
            delivery_accounts = cursor.fetchall()
            
            # 서류 첨부 정보 조회
            cursor.execute("SELECT doc_name, uploaded_time FROM documents WHERE client_id = ?", (client_data[0],))
            documents = cursor.fetchall()
            
            result = {
                'client': client_data,
                'delivery_accounts': delivery_accounts,
                'documents': documents
            }
        
        conn.close()
        return result