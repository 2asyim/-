class TextFormatters:
    @staticmethod
    def format_rrn(text):
        """주민등록번호 포맷팅: '000000-0000000'"""
        # 하이픈 제거
        text = text.replace("-", "")
        
        # 숫자만 필터링
        text = ''.join(char for char in text if char.isdigit())
        
        # 입력 길이 제한 (최대 13자리)
        if len(text) > 13:
            text = text[:13]
        
        # 하이픈 추가
        if len(text) > 6:
            text = text[:6] + "-" + text[6:]
            
        return text
            
    @staticmethod
    def format_phone(text):
        """전화번호 포맷팅: '000-0000-0000'"""
        # 하이픈 제거
        text = text.replace("-", "")
        
        # 숫자만 필터링
        text = ''.join(char for char in text if char.isdigit())
        
        # 최대 11자리로 제한
        if len(text) > 11:
            text = text[:11]
        
        # 하이픈 추가
        if len(text) >= 10:
            text = f"{text[:3]}-{text[3:7]}-{text[7:11]}"
        elif len(text) >= 7:
            text = f"{text[:3]}-{text[3:6]}-{text[6:]}"
        elif len(text) >= 4:
            text = f"{text[:3]}-{text[3:]}"
            
        return text
            
    @staticmethod
    def format_biznum(text):
        """사업자등록번호 포맷팅: '000-00-00000'"""
        # 하이픈 제거
        text = text.replace("-", "")
        
        # 숫자만 필터링
        text = ''.join(char for char in text if char.isdigit())
        
        # 최대 10자리로 제한
        if len(text) > 10:
            text = text[:10]
        
        # 하이픈 추가
        if len(text) > 5:
            text = f"{text[:3]}-{text[3:5]}-{text[5:10]}"
        elif len(text) > 3:
            text = f"{text[:3]}-{text[3:5]}"
            
        return text
            
    @staticmethod
    def format_number_with_commas(text):
        """숫자에 천 단위 쉼표 추가"""
        # 쉼표 제거
        text = text.replace(",", "")
        
        # 숫자만 필터링
        text = ''.join(char for char in text if char.isdigit())
        
        # 숫자가 있을 때만 포맷팅
        if text:
            return f"{int(text):,}"
        return ""