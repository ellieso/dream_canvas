class PromptBuilder:
    """프롬프트를 생성하는 클래스"""
    
    def build_prompt(self, dream_text, dream_type, keywords):
        """꿈 내용에 기반하여 이미지 생성 프롬프트 생성"""
        
        # 일상적 꿈과 환상적 꿈 구분 처리
        is_mundane_dream = dream_type in ["일상", "음식", "가족"]
        
        # 꿈 유형별 기본 프롬프트
        type_prompts = {
            "음식": "a realistic scene of people eating or enjoying food",
            "비행": "a person flying or floating through the air, dreamlike view from above",
            "추락": "a person falling through the air, vertigo-inducing perspective",
            "추격": "being chased in a tense dream scene, running away from something",
            "수중": "underwater dreamscape, submerged in water, swimming in deep waters",
            "괴물": "encountering strange creatures or monsters in a dream, eerie atmosphere",
            "시험": "stressful academic setting, examination hall, feeling unprepared",
            "일상": "everyday dream scene with slight surreal elements, familiar setting",
            "판타지": "magical fantasy dreamscape with mythical elements",
            "일반": "surreal dream scene with symbolic elements",
            "미래": "futuristic dream environment with advanced technology",
            "과거": "historical or ancient dream setting with period elements",
            "가족": "family gathering or family-related dream scene with emotional elements",
            "여행": "travel or journey scene with exploration elements",
        }
        
        # 복합 유형 처리
        if dream_type.startswith("mixed_"):
            types = dream_type.split("_")[1:]
            base_elements = []
            for t in types:
                if t in type_prompts:
                    base_elements.append(type_prompts[t])
            
            base = ", ".join(base_elements) if base_elements else type_prompts["일반"]
        else:
            base = type_prompts.get(dream_type, type_prompts["일반"])
        
        # 키워드 처리 - 한글 키워드와 영어 키워드 분리
        eng_keywords = []
        for keyword in keywords:
            if all(ord(c) < 128 for c in keyword):
                eng_keywords.append(keyword)
        
        # 영어 키워드가 너무 많으면 최대 8개로 제한
        if len(eng_keywords) > 8:
            eng_keywords = eng_keywords[:8]
        
        # "떡볶이" 특별 처리
        if "떡볶이" in dream_text:
            if "tteokbokki" not in eng_keywords and "korean spicy rice cake" not in eng_keywords:
                eng_keywords.insert(0, "tteokbokki, korean spicy rice cake dish")
        
        # "친구" 특별 처리
        if "친구" in dream_text:
            if "friend" not in eng_keywords and "friends" not in eng_keywords:
                eng_keywords.insert(0, "friends")
        
        # 프롬프트 구성
        prompt_parts = []
        
        # 일상적 꿈과 환상적 꿈 구분하여 프롬프트 생성
        if is_mundane_dream:
            # 일상적 꿈용 프롬프트 (더 사실적)
            prompt_parts.append(f"A realistic scene depicting {base}")
            
            if eng_keywords:
                keyword_text = ", ".join(eng_keywords)
                prompt_parts.append(f"showing {keyword_text}")
            
            # 일상적 품질 요소 (dreamlike/surreal 요소 제거)
            prompt_parts.append("natural lighting, clear details, realistic style")
            prompt_parts.append("photographic quality, everyday life, normal scene")
            
        else:
            # 환상적 꿈용 프롬프트 (기존 방식)
            prompt_parts.append(f"A vivid dream scene depicting {base}")
            
            if eng_keywords:
                keyword_text = ", ".join(eng_keywords)
                prompt_parts.append(f"with elements of {keyword_text}")
            
            # 환상적 품질 요소
            prompt_parts.append("dreamlike atmosphere, surreal quality, ethereal feeling")
            prompt_parts.append("detailed illustration, dreamscape, cinematic lighting")
        
        # 최종 프롬프트
        final_prompt = ", ".join(prompt_parts)
        
        return final_prompt