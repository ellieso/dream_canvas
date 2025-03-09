import os
import sys
import streamlit as st
from PIL import Image
import io
import time
import threading

# 세션 상태 초기화
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'dream_result' not in st.session_state:
    st.session_state.dream_result = None
if 'dream_image' not in st.session_state:
    st.session_state.dream_image = None
if 'dream_info' not in st.session_state:
    st.session_state.dream_info = {}
if 'dream_text' not in st.session_state:
    st.session_state.dream_text = ""

# 현재 스크립트의 디렉토리를 기준으로 상위 디렉토리를 모듈 검색 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 상대 경로로 모듈 import
try:
    from dream.analyzer import DreamAnalyzer
    from dream.interpreter import DreamInterpreter
    from generation.image_generator import ImageGenerator
    from generation.prompt_builder import PromptBuilder
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info(f"Current directory: {current_dir}")
    st.info(f"Python path: {sys.path}")
    st.stop()

# 꿈 분석 함수
def process_dream(dream_text):
    # 초기 상태
    progress_placeholder = st.empty()
    status_container = st.empty()
    
    # 진행 단계 표시 (0%)
    progress_bar = progress_placeholder.progress(0)
    status_container.info("🔍 꿈 분석을 시작합니다...")
    time.sleep(1)  # 각 단계 사이에 약간의 지연 추가
    
    # 1단계: 꿈 분석 준비 (10%)
    progress_bar.progress(10)
    status_container.info("🔍 꿈 분석을 준비하는 중...")
    time.sleep(1)
    
    # 2단계: 꿈 분석 중 (25%)
    progress_bar.progress(25)
    status_container.info("🔍 꿈을 분석하는 중...")
    
    # 꿈 분석
    analyzer = DreamAnalyzer()
    dream_type, keywords = analyzer.analyze(dream_text)
    time.sleep(1)
    
    # 3단계: 프롬프트 생성 준비 (40%)
    progress_bar.progress(40)
    status_container.info("✨ 이미지 생성 프롬프트를 준비하는 중...")
    time.sleep(1)
    
    # 4단계: 프롬프트 생성 중 (50%)
    progress_bar.progress(50)
    status_container.info("✨ 이미지 생성 프롬프트를 구성하는 중...")
    
    # 프롬프트 생성
    prompt_builder = PromptBuilder()
    prompt = prompt_builder.build_prompt(dream_text, dream_type, keywords)
    time.sleep(1)
    
    # 5단계: 이미지 생성 준비 (60%)
    progress_bar.progress(60)
    status_container.info("🎨 꿈 시각화를 준비하는 중...")
    time.sleep(1)

    # 6단계: 이미지 생성 시작 (75%)
    progress_bar.progress(75)
    status_container.info("🎨 이미지 생성 준비 중...")
    time.sleep(1)

    # 이미지 생성 알림
    progress_bar.progress(80)
    status_container.warning("🎨 꿈을 시각화하는 중... 잠시만 기다려주세요 (약 30초 소요)")
    
    # 이미지 생성
    generator = ImageGenerator()
    image = generator.generate(prompt)
    
    # 7단계: 마무리 중 (90%)
    progress_bar.progress(90)
    status_container.info("✅ 결과를 준비하는 중...")
    time.sleep(1)
    
    # 8단계: 완료 (100%)
    progress_bar.progress(100)
    status_container.success("✅ 꿈 해석 및 시각화 완료!")
    time.sleep(1)
    
    # 진행 바 제거
    progress_placeholder.empty()
    status_container.empty()
    
    # 꿈 해석
    interpreter = DreamInterpreter()
    interpretation = interpreter.interpret(dream_text, dream_type, keywords)
    
    # 세션 상태에 결과 저장
    st.session_state.processed = True
    st.session_state.dream_text = dream_text
    st.session_state.dream_result = interpretation
    st.session_state.dream_image = image
    st.session_state.dream_info = {
        "dream_type": dream_type,
        "keywords": keywords,
        "prompt": prompt
    }
    
    # 페이지 리로드
    st.rerun()

def main():
    st.set_page_config(
        page_title="Dream Canvas",
        page_icon="✨",
        layout="wide"
    )
    
    st.title("✨ Dream Canvas")
    st.markdown("당신의 소중한 꿈의 기억을 입력해주세요. 아름다운 이미지와 해석 결과를 알려드릴게요!")
    
    # 사이드바에 정보 표시
    st.sidebar.title("About")
    st.sidebar.info(
        "이 앱은 Stable Diffusion을 사용하여 꿈을 시각화하고 해석합니다.\n\n"
        "모델: Stable Diffusion v1.5\n"
        "개발: AI 생성 기술 활용 프로젝트"
    )
    
    # 결과가 이미 있으면 표시
    if st.session_state.processed:
        # 새 꿈 분석 버튼
        if st.button("새로운 꿈 분석하기", key="new_dream"):
            st.session_state.processed = False
            st.rerun()
        
        # 텍스트 표시
        st.info(f"입력한 꿈: {st.session_state.dream_text}")
        
        # 결과 표시
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 이미지 표시
            st.subheader("🖼️ 꿈 시각화")
            st.image(st.session_state.dream_image, use_container_width=True)
            
            # 이미지 다운로드 버튼
            buf = io.BytesIO()
            st.session_state.dream_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # 버튼 스타일링 및 전체 너비로 설정
            st.markdown("""
            <style>
            div.stDownloadButton > button {
                width: 100%;
                background-color: #4CAF50;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            div.stDownloadButton > button:hover {
                background-color: #45a049;
            }
            </style>
            """, unsafe_allow_html=True)

            st.download_button(
                label="🖼️ 이미지 다운로드",
                data=byte_im,
                file_name="dream_image.png",
                mime="image/png",
                use_container_width=True,
                key="download_button"
            )
        
        with col2:
            st.subheader("📝 꿈 해석 결과")

            # 해석 결과 가독성 개선
            interpretation = st.session_state.dream_result
            if "【꿈의 유형】" in interpretation:
                # 꿈의 유형 부분만 표시
                type_part = interpretation.split("【꿈의 상징 해석】")[0].strip()
                st.write(type_part)
            else:
                # 포맷팅되지 않은 경우 원본 그대로 출력
                st.write(interpretation)
            
            # 분석 정보
            with st.expander("분석 정보 보기"):
                st.write(f"**꿈 유형**: {st.session_state.dream_info['dream_type']}")
                st.write(f"**감지된 키워드**: {', '.join(st.session_state.dream_info['keywords']) if st.session_state.dream_info['keywords'] else '없음'}")
                st.write(f"**생성 프롬프트**: {st.session_state.dream_info['prompt']}")
    else:
        # 사용자 입력
        st.markdown("#### 당신의 꿈에 대해 설명해주세요")
        dream_text = st.text_area("", placeholder="꿈 내용을 입력하고 Enter 키를 누르세요", height=150)

        # 실행 조건 (텍스트가 입력된 경우)
        if dream_text:
            # 세션 상태를 사용하여 텍스트가 변경되었는지 확인
            if 'previous_text' not in st.session_state:
                st.session_state.previous_text = ""
            
            # 텍스트가 변경되었고 이전에 처리되지 않은 경우 자동 실행
            if dream_text != st.session_state.previous_text and dream_text.strip():
                st.session_state.previous_text = dream_text
                try:
                    process_dream(dream_text)
                except Exception as e:
                    st.error(f"처리 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()