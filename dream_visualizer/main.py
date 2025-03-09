from dream.analyzer import DreamAnalyzer
from dream.interpreter import DreamInterpreter
from generation.image_generator import ImageGenerator
from generation.prompt_builder import PromptBuilder
from utils.helpers import log_execution_time, get_user_confirmation

@log_execution_time
def main():
    print("===== 꿈 시각화 및 해몽 시스템 =====")
    
    # 사용자 입력
    dream_text = input("꿈에 대해 설명해주세요: ")
    
    # 꿈 분석
    analyzer = DreamAnalyzer()
    dream_type, keywords = analyzer.analyze(dream_text)
    print(f"분석된 꿈 유형: {dream_type}")
    print(f"추출된 키워드: {', '.join(keywords) if keywords else '없음'}")
    
    # 프롬프트 생성
    prompt_builder = PromptBuilder()
    prompt = prompt_builder.build_prompt(dream_text, dream_type, keywords)
    
    # 이미지 생성 확인
    if get_user_confirmation("이미지를 생성하시겠습니까? (y/n): "):
        # 이미지 생성
        generator = ImageGenerator()
        image = generator.generate(prompt)
    
    # 꿈 해석
    interpreter = DreamInterpreter()
    interpretation = interpreter.interpret(dream_text, dream_type, keywords)
    
    # 결과 출력
    print("\n✨ 꿈 해몽 결과:")
    print(interpretation)

if __name__ == "__main__":
    main()