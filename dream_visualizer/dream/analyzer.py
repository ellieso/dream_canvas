from dream.keywords import DREAM_TYPES, KEYWORDS_MAP

class DreamAnalyzer:
    """꿈 내용을 분석하는 클래스"""
    
    def analyze(self, dream_text):
        """
        꿈 설명을 분석하여 유형과 키워드를 추출
        
        Args:
            dream_text (str): 사용자가 입력한 꿈 설명
            
        Returns:
            tuple: (꿈_유형, 키워드_리스트)
        """
        # 입력 텍스트 전처리
        processed_text = dream_text.lower()
        
        # 꿈 유형 판단을 위한 점수 계산
        type_scores = {}
        matched_keywords = []
        
        # 각 유형별 점수 계산
        for type_name, markers in DREAM_TYPES.items():
            score = 0
            type_keywords = []
            
            for marker in markers:
                if marker in processed_text:
                    # 마커가 발견되면 점수 증가
                    score += 1
                    # 발견된 키워드 추가
                    type_keywords.append(marker)
                    
                    # 전체 키워드 목록에 없으면 추가
                    if marker not in matched_keywords:
                        matched_keywords.append(marker)
            
            # 점수가 있는 경우만 기록
            if score > 0:
                type_scores[type_name] = {
                    'score': score,
                    'keywords': type_keywords
                }
        
        # 추가 키워드를 영어로 변환
        english_keywords = []
        for keyword in matched_keywords:
            # KEYWORDS_MAP에 있는 키워드는 영어로 변환
            if keyword in KEYWORDS_MAP:
                english_keywords.append(KEYWORDS_MAP[keyword])
        
        # 일반 키워드 맵 검색 (개별 단어 처리)
        words = processed_text.split()
        for word in words:
            if word in KEYWORDS_MAP and word not in matched_keywords:
                matched_keywords.append(word)
                english_keywords.append(KEYWORDS_MAP[word])
        
        # 최상위 꿈 유형 결정
        dream_type = "일반"
        if type_scores:
            # 점수가 가장 높은 유형 찾기
            top_type = max(type_scores.items(), key=lambda x: x[1]['score'])
            dream_type = top_type[0]
        
        # 복합 유형 처리
        complex_type = False
        secondary_types = []
        
        if len(type_scores) > 1:
            sorted_types = sorted(type_scores.items(), key=lambda x: x[1]['score'], reverse=True)
            top_score = sorted_types[0][1]['score']
            
            # 점수 차이가 1 이하인 차상위 유형들 추가
            for t, info in sorted_types[1:]:
                if top_score - info['score'] <= 1:
                    secondary_types.append(t)
                    complex_type = True
        
        # 디버깅 정보
        # print(f"분석된 점수: {type_scores}")
        # if complex_type:
        #     print(f"주요 유형: {dream_type}, 부가 유형: {', '.join(secondary_types)}")
        
        # 복합 유형인 경우 mixed_type 형태로 반환
        if complex_type and secondary_types:
            final_type = f"mixed_{dream_type}"
            for t in secondary_types[:2]:  # 최대 2개까지만 혼합
                final_type += f"_{t}"
        else:
            final_type = dream_type
        
        # 모든 가용한 키워드 반환 (한글 키워드와 영어 키워드 모두)
        all_keywords = matched_keywords + english_keywords
        
        return final_type, all_keywords