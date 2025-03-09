from diffusers import StableDiffusionPipeline
import torch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_ID, NUM_INFERENCE_STEPS, GUIDANCE_SCALE, OUTPUT_IMAGE_PATH, USE_HALF_PRECISION

class ImageGenerator:
    """Stable Diffusion을 사용하여 이미지를 생성하는 클래스"""
    
    def __init__(self):
        """이미지 생성기 초기화"""
        self.model_id = MODEL_ID
        self.pipeline = None
    
    def load_model(self):
        """Stable Diffusion 모델 로드"""
        # 모델이 이미 로드되었는지 확인
        if self.pipeline is not None:
            return
        
        # 데이터 타입 설정
        dtype = torch.float16 if USE_HALF_PRECISION else torch.float32
        
        # 모델 로드
        print("모델 로드 중...")
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=dtype
        )
        
        # Apple Silicon 맥용 설정
        if torch.backends.mps.is_available():
            device = "mps"
            self.pipeline = self.pipeline.to(device)
            print("MPS 장치를 사용합니다.")
        else:
            print("MPS 장치를 찾을 수 없습니다. CPU로 실행됩니다.")

    def generate(self, prompt, steps=None, guidance_scale=None):
        """
        프롬프트를 기반으로 이미지 생성
        """
        # 모델 로드
        self.load_model()
        
        # 기본값 설정
        steps = steps or NUM_INFERENCE_STEPS
        guidance_scale = guidance_scale or GUIDANCE_SCALE
        
        # 이미지 생성
        image = self.pipeline(
            prompt,
            num_inference_steps=steps,
            guidance_scale=guidance_scale
        ).images[0]
        
        # Streamlit에서는 이미지를 반환
        return image
    
    # def generate(self, prompt, steps=None, guidance_scale=None):
    #     """
    #     프롬프트를 기반으로 이미지 생성
        
    #     Args:
    #         prompt (str): 이미지 생성용 프롬프트
    #         steps (int, optional): 추론 단계 수
    #         guidance_scale (float, optional): 프롬프트 가이던스 스케일
            
    #     Returns:
    #         PIL.Image: 생성된 이미지
    #     """
    #     # 모델 로드
    #     self.load_model()
        
    #     # 기본값 설정
    #     steps = steps or NUM_INFERENCE_STEPS
    #     guidance_scale = guidance_scale or GUIDANCE_SCALE
        
    #     # 프롬프트 출력
    #     print(f"프롬프트: {prompt}")
    #     print(f"이미지 생성 중... (단계: {steps}, 가이던스: {guidance_scale})")
        
    #     # 이미지 생성
    #     image = self.pipeline(
    #         prompt,
    #         num_inference_steps=steps,
    #         guidance_scale=guidance_scale
    #     ).images[0]
        
    #     # 이미지 저장
    #     image.save(OUTPUT_IMAGE_PATH)
    #     print(f"이미지가 '{OUTPUT_IMAGE_PATH}'로 저장되었습니다.")
        
    #     return image