"""
TTS (Text-to-Speech) 서비스
라즈베리파이 스피커로 음성 출력
"""
import os
import tempfile
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def play_tts(text: str, lang: str = 'ko') -> None:
    """
    텍스트를 음성으로 변환하여 라즈베리파이 스피커로 재생

    Args:
        text: 변환할 텍스트
        lang: 언어 코드 (기본값: 'ko')

    Raises:
        Exception: TTS 재생 실패 시
    """
    try:
        # 방법 1: gTTS 사용 (인터넷 필요)
        try:
            from gtts import gTTS
            import pygame

            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name

            # TTS 생성
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_file)

            # pygame으로 재생
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # 재생 완료까지 대기
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # 정리
            pygame.mixer.quit()
            os.remove(temp_file)

            logger.info(f"TTS 재생 완료 (gTTS): {text[:50]}...")
            return

        except ImportError:
            logger.warning("gTTS 또는 pygame이 설치되지 않음. espeak 시도...")

        # 방법 2: espeak 사용 (오프라인, Linux 전용)
        try:
            import subprocess

            # espeak 명령어로 직접 재생
            # -v: 언어/목소리, -s: 속도 (기본 175)
            voice = 'ko' if lang == 'ko' else 'en'
            subprocess.run(['espeak', '-v', voice, '-s', '150', text], check=True)

            logger.info(f"TTS 재생 완료 (espeak): {text[:50]}...")
            return

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            logger.warning(f"espeak 실행 실패: {e}")

        # 방법 3: pyttsx3 사용 (오프라인, 크로스 플랫폼)
        try:
            import pyttsx3

            engine = pyttsx3.init()

            # 한국어 음성 설정 (가능한 경우)
            if lang == 'ko':
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'korean' in voice.name.lower() or 'ko' in voice.languages:
                        engine.setProperty('voice', voice.id)
                        break

            engine.setProperty('rate', 150)  # 속도
            engine.setProperty('volume', 1.0)  # 볼륨

            engine.say(text)
            engine.runAndWait()

            logger.info(f"TTS 재생 완료 (pyttsx3): {text[:50]}...")
            return

        except ImportError:
            logger.warning("pyttsx3가 설치되지 않음")

        # 모든 방법 실패
        raise Exception("TTS 라이브러리가 설치되지 않았습니다. gTTS, espeak, 또는 pyttsx3를 설치하세요.")

    except Exception as e:
        logger.error(f"TTS 재생 오류: {str(e)}")
        raise
