import time

def log_execution_time(func):
    """함수 실행 시간을 로깅하는 데코레이터"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 실행 시간: {end_time - start_time:.2f}초")
        return result
    return wrapper

def clean_text(text):
    """입력 텍스트 정리"""
    return text.strip().lower()

def get_user_confirmation(message="계속하시겠습니까? (y/n): "):
    """사용자 확인 얻기"""
    response = input(message).strip().lower()
    return response == 'y' or response == 'yes'