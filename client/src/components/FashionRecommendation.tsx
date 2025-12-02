import { useState, useEffect, useRef } from 'react';
import { Volume2, Play, Pause, Sparkles, Loader2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Skeleton } from './ui/skeleton';

interface FashionRecommendationData {
  text: string;
}

interface FashionRecommendationProps {
  recommendation: FashionRecommendationData | null;
  isLoading: boolean;
}

export default function FashionRecommendation({ recommendation, isLoading }: FashionRecommendationProps) {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTypingComplete, setIsTypingComplete] = useState(false);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  // ------------------------------
  // 🔵 타이핑 애니메이션
  // ------------------------------
  useEffect(() => {
    if (!recommendation) return;

    setDisplayedText('');
    setCurrentIndex(0);
    setIsTypingComplete(false);

    const typingInterval = setInterval(() => {
      setCurrentIndex(prev => {
        if (prev < recommendation.text.length) {
          setDisplayedText(recommendation.text.slice(0, prev + 1));
          return prev + 1;
        } else {
          clearInterval(typingInterval);
          setIsTypingComplete(true);
          return prev;
        }
      });
    }, 30);

    return () => clearInterval(typingInterval);
  }, [recommendation]);

  // ------------------------------
  // 🔊 TTS 기능
  // ------------------------------
  const handleSpeak = () => {
    if (!recommendation) return;

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(recommendation.text);
    utterance.lang = 'ko-KR';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  };

  // ==========================================================
  // 🟣 새로운 로딩 UI (원본 디자인 유지하면서만 개선)
  // ==========================================================
  if (isLoading) {
    return (
      <Card className="shadow-2xl border-0 bg-white/90 backdrop-blur-md h-full">
        <CardHeader className="pb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-500" />
            <CardTitle>패션 추천</CardTitle>
          </div>
        </CardHeader>

        <CardContent className="space-y-5">
          <div className="flex flex-col items-center text-center py-10">
            <Loader2 className="w-10 h-10 text-purple-500 animate-spin mb-4" />
            <p className="text-gray-700 font-medium">AI 추천 생성 중…</p>
            <p className="text-gray-500 text-sm">기온·습도·날씨를 분석하고 있어요</p>
          </div>

          {/* 기존 skeleton 줄 유지 */}
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-4/6" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
        </CardContent>
      </Card>
    );
  }

  // ==========================================================
  // 🟣 추천 내용 표시 (기존 디자인 완전 유지)
  // ==========================================================
  if (!recommendation) return null;

  return (
    <Card className="shadow-2xl border-0 bg-gradient-to-br from-purple-500/90 to-pink-500/90 backdrop-blur-md h-full text-white hover:shadow-3xl transition-shadow">
      <CardHeader className="pb-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-yellow-300" />
            <CardTitle className="text-white">오늘의 패션 추천</CardTitle>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={handleSpeak}
            className="rounded-full bg-white/20 hover:bg-white/30 text-white h-10 w-10"
          >
            {isSpeaking ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="relative min-h-[300px] p-6 bg-white/10 backdrop-blur-sm rounded-xl border border-white/20">
          <p className="text-white leading-relaxed text-base">
            {displayedText}
            {!isTypingComplete && (
              <span className="inline-block w-0.5 h-5 bg-white ml-1 animate-pulse" />
            )}
          </p>
        </div>

        {isSpeaking && (
          <div className="flex items-center justify-center gap-2 bg-white/20 text-white px-4 py-2 rounded-full backdrop-blur-sm">
            <Volume2 className="w-4 h-4 animate-pulse" />
            <span className="text-sm font-medium">음성 재생 중...</span>
          </div>
        )}

        {!isSpeaking && isTypingComplete && (
          <div className="flex items-center justify-center gap-2 text-white/80 text-sm">
            <Volume2 className="w-4 h-4" />
            <span>음성으로 듣기</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
