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
        # 방법 1: gTTS + 시스템 오디오 플레이어 (최우선, 음질 좋음)
        try:
            from gtts import gTTS
            import subprocess

            # 임시 파일 생성
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name

            # TTS 생성
            logger.info(f"gTTS로 음성 생성 중: {text[:50]}...")
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_file)

            # 시스템 명령어로 재생
            # ffplay: 블루투스 포함 모든 오디오 장치 지원, 오류 메시지 최소화
            # -loglevel panic: 오류 메시지 숨김
            players = [
                ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'panic', temp_file],  # 최우선 (블루투스 지원)
                ['mpg123', '-q', temp_file],  # 대체
                ['cvlc', '--play-and-exit', '--quiet', temp_file],  # 대체2
            ]

            played = False
            for player_cmd in players:
                try:
                    subprocess.run(player_cmd, check=True, timeout=30,
                                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    played = True
                    logger.info(f"TTS 재생 완료 (gTTS + {player_cmd[0]}): {text[:50]}...")
                    break
                except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    continue

            # 정리
            if os.path.exists(temp_file):
                os.remove(temp_file)

            if played:
                return
            else:
                logger.warning("오디오 플레이어를 찾을 수 없음 (ffplay, mpg123, cvlc). espeak 시도...")

        except ImportError:
            logger.warning("gTTS가 설치되지 않음. espeak 시도...")
        except Exception as e:
            logger.warning(f"gTTS 실행 중 오류: {e}, espeak 시도...")

        # 방법 2: espeak 사용 (오프라인, 폴백)
        try:
            import subprocess

            # espeak 명령어로 직접 재생
            voice = 'ko' if lang == 'ko' else 'en'
            subprocess.run(['espeak', '-v', voice, '-s', '150', text], check=True)

            logger.info(f"TTS 재생 완료 (espeak): {text[:50]}...")
            return

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            logger.warning(f"espeak 실행 실패: {e}")

        # 모든 방법 실패
        raise Exception("TTS 재생 실패: gTTS는 설치되었지만 오디오 플레이어(mpg123, ffplay, cvlc)가 없습니다. 'sudo apt-get install mpg123' 실행하세요.")

    except Exception as e:
        logger.error(f"TTS 재생 오류: {str(e)}")
        raise
