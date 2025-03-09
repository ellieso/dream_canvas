from dream.keywords import DREAM_SYMBOLS

class DreamInterpreter:
    """꿈을 해석하는 클래스"""
    
    def interpret(self, dream_text, dream_type, keywords):
        """
        꿈을 분석하여 해석 결과를 제공
        
        Args:
            dream_text (str): 사용자가 입력한 꿈 설명
            dream_type (str): 분석된 꿈 유형
            keywords (list): 추출된 키워드 목록
            
        Returns:
            str: 꿈 해석 결과
        """
        # 꿈 유형별 일반적 해석
        type_interpretations = {
            "비행": "하늘을 나는 꿈은 자유와 해방감에 대한 갈망, 또는 상황을 높은 관점에서 보고 싶은 욕구를 나타냅니다.",
            "추락": "추락하는 꿈은 통제력 상실에 대한 두려움이나 불안감, 자신감 저하를 상징할 수 있습니다.",
            "추격": "쫓기는 꿈은 현실에서 회피하고 있는 문제나 스트레스를 상징하는 경우가 많습니다.",
            "수중": "물 속에서의 꿈은 감정적인 상태나 무의식 세계를 탐험하는 것을 나타냅니다.",
            "괴물": "괴물이 등장하는 꿈은 내면의 두려움이나 극복해야 할 부정적 측면을 상징합니다.",
            "시험": "시험에 관한 꿈은 평가에 대한 불안이나 준비 부족에 대한 걱정을 나타냅니다.",
            "일상": "일상적인 장면의 꿈은 현재 삶의 특정 측면을 재평가하고 있음을 나타낼 수 있습니다.",
            "판타지": "환상적인 꿈은 창의성, 상상력, 또는 현실에서 충족되지 않는 욕구를 상징합니다.",
            "일반": "이 꿈은 당신의 무의식이 전달하려는 메시지를 담고 있습니다."
        }
        
        # 결과 조합
        interpretation = []
        
        # 1. 꿈 유형 해석 추가
        if dream_type in type_interpretations:
            interpretation.append(f"【꿈의 유형】 {dream_type}")
            interpretation.append(type_interpretations[dream_type])
        
        # 2. 개별 상징 해석 추가
        symbol_found = False
        interpretation.append("\n【꿈의 상징 해석】")
        
        for keyword in keywords:
            if keyword in DREAM_SYMBOLS:
                symbol_found = True
                interpretation.append(f"'{keyword}': {DREAM_SYMBOLS[keyword]}")
        
        # 상징을 찾지 못한 경우
        if not symbol_found:
            for keyword in dream_text.split():
                if keyword in DREAM_SYMBOLS:
                    symbol_found = True
                    interpretation.append(f"'{keyword}': {DREAM_SYMBOLS[keyword]}")
        
        if not symbol_found:
            interpretation.append("특정 상징에 대한 해석을 찾을 수 없습니다.")
        
        return "\n".join(interpretation)