"""
TTS (Text-to-Speech) 서비스
라즈베리파이 스피커로 음성 출력
"""
import os
import tempfile
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# 현재 재생 중인 프로세스 추적
current_tts_process = None

def stop_tts() -> None:
    """
    현재 재생 중인 TTS 중단
    """
    global current_tts_process

    if current_tts_process and current_tts_process.poll() is None:
        print(f"[TTS] 🛑 재생 중단 요청")
        current_tts_process.kill()
        current_tts_process.wait()
        current_tts_process = None
        print(f"[TTS] ✅ 재생 중단 완료")
    else:
        print(f"[TTS] ℹ️  재생 중인 TTS 없음")


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
            print(f"[TTS] gTTS로 음성 생성 중: {text[:50]}...")
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_file)
            print(f"[TTS] MP3 파일 생성 완료: {temp_file}")

            # 시스템 명령어로 재생
            # ffplay: 블루투스 포함 모든 오디오 장치 지원, 오류 메시지 최소화
            # -loglevel panic: 오류 메시지 숨김
            players = [
                ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'panic', temp_file],  # 최우선 (블루투스 지원)
                ['mpg123', '-q', temp_file],  # 대체
                ['cvlc', '--play-and-exit', '--quiet', temp_file],  # 대체2
            ]

            played = False
            global current_tts_process

            for player_cmd in players:
                try:
                    print(f"[TTS] 재생 시도: {' '.join(player_cmd)}")

                    # 환경 변수 설정: PulseAudio 사용 강제
                    env = os.environ.copy()
                    env['SDL_AUDIODRIVER'] = 'pulseaudio'  # SDL(ffplay)에서 PulseAudio 사용
                    env['AUDIODEV'] = 'pulse'              # 오디오 장치를 pulse로
                    if 'PULSE_SERVER' not in env:
                        env['PULSE_SERVER'] = '/run/user/1000/pulse/native'  # PulseAudio 서버 주소

                    # 타임아웃: 텍스트 길이에 따라 동적 조정 (최소 120초로 증가)
                    timeout_seconds = max(120, len(text) // 10)  # 텍스트 10자당 1초, 최소 120초

                    # Popen 사용 (중단 가능하도록)
                    current_tts_process = subprocess.Popen(
                        player_cmd,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        env=env
                    )

                    # 재생 완료까지 대기
                    try:
                        current_tts_process.wait(timeout=timeout_seconds)
                        played = True
                        print(f"[TTS] ✅ 재생 완료 ({player_cmd[0]}): {text[:50]}...")
                    except subprocess.TimeoutExpired:
                        print(f"[TTS] ❌ {player_cmd[0]} 타임아웃")
                        current_tts_process.kill()
                        current_tts_process = None
                        continue

                    current_tts_process = None
                    break
                except FileNotFoundError as e:
                    print(f"[TTS] ❌ {player_cmd[0]} 찾을 수 없음")
                    continue
                except subprocess.CalledProcessError as e:
                    print(f"[TTS] ❌ {player_cmd[0]} 실행 오류: returncode={e.returncode}")
                    if e.stderr:
                        print(f"[TTS] stderr: {e.stderr.decode()}")
                    continue
                except subprocess.TimeoutExpired as e:
                    print(f"[TTS] ❌ {player_cmd[0]} 타임아웃")
                    continue

            # 정리
            if os.path.exists(temp_file):
                os.remove(temp_file)

            if played:
                return
            else:
                print(f"[TTS] ❌ 오디오 플레이어를 찾을 수 없음 (ffplay, mpg123, cvlc). espeak 시도...")

        except ImportError:
            print(f"[TTS] ❌ gTTS가 설치되지 않음. espeak 시도...")
        except Exception as e:
            print(f"[TTS] ❌ gTTS 실행 중 오류: {e}, espeak 시도...")

        # 방법 2: espeak 사용 (오프라인, 폴백)
        try:
            import subprocess

            # espeak 명령어로 직접 재생
            voice = 'ko' if lang == 'ko' else 'en'
            print(f"[TTS] espeak으로 재생 시도...")
            subprocess.run(['espeak', '-v', voice, '-s', '150', text], check=True)

            print(f"[TTS] ✅ TTS 재생 완료 (espeak): {text[:50]}...")
            return

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"[TTS] ❌ espeak 실행 실패: {e}")

        # 모든 방법 실패
        raise Exception("TTS 재생 실패: gTTS는 설치되었지만 오디오 플레이어(mpg123, ffplay, cvlc)가 없습니다. 'sudo apt-get install mpg123' 실행하세요.")

    except Exception as e:
        print(f"[TTS] ❌ TTS 재생 오류: {str(e)}")
        raise
