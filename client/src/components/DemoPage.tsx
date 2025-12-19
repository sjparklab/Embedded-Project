import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Loader2, ArrowLeft } from 'lucide-react';

interface DemoPageProps {
  onBack: () => void;
}

export default function DemoPage({ onBack }: DemoPageProps) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ text: string; keyword: string } | null>(null);
  const [currentScenario, setCurrentScenario] = useState<string>("");

  const scenarios = [
    {
      name: "비 오는 날 (우산)",
      mode: "fashion",
      data: {
        temperature: 18,
        humidity: 90,
        weather: "Rain",
        description: "비가 내림",
        location: "가상 서울",
        co2: 450
      }
    },
    {
      name: "폭염 (더위)",
      mode: "fashion",
      data: {
        temperature: 35,
        humidity: 50,
        weather: "Clear",
        description: "맑고 매우 더움",
        location: "가상 대구",
        co2: 400
      }
    },
    {
      name: "한파 (추위)",
      mode: "fashion",
      data: {
        temperature: -10,
        humidity: 30,
        weather: "Snow",
        description: "눈이 오고 추움",
        location: "가상 철원",
        co2: 400
      }
    },
    {
      name: "실내 공기 나쁨 (환기)",
      mode: "environment",
      data: {
        temperature: 24,
        humidity: 70,
        weather: "Cloudy",
        description: "흐림",
        location: "가상 부산",
        co2: 2500 // 매우 높음
      }
    },
    {
      name: "쾌적한 실내 (난방 필요)",
      mode: "environment",
      data: {
        temperature: 15, // 약간 추움
        humidity: 40,
        weather: "Clear",
        description: "맑음",
        location: "가상 서울",
        co2: 450
      }
    }
  ];

  const handleScenarioClick = async (scenario: any) => {
    setLoading(true);
    setCurrentScenario(scenario.name);
    setResult(null);

    try {
      const res = await fetch("/api/demo/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mode: scenario.mode,
          weatherData: scenario.data
        })
      });
      const json = await res.json();
      if (json.success) {
        setResult({ text: json.text, keyword: json.keyword });
      } else {
        setResult({ text: "오류 발생: " + json.error, keyword: "ERROR" });
      }
    } catch (err) {
      console.error(err);
      setResult({ text: "통신 오류 발생", keyword: "ERROR" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-4">
        <Button variant="outline" onClick={onBack} className="rounded-full w-10 h-10 p-0">
          <ArrowLeft className="w-5 h-5" />
        </Button>
        <h2 className="text-2xl font-bold text-white drop-shadow-md">
          시스템 데모 / 테스트 모드
        </h2>
      </div>

      <h3 className="text-xl font-bold text-white drop-shadow-md mb-4">시나리오 선택</h3>
      <Card className="bg-white backdrop-blur border-0" style={{ borderRadius: '1rem', boxShadow: '0 10px 40px rgba(0,0,0,0.15)' }}>
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {scenarios.map((scenario, idx) => (
              <Button
                key={idx}
                variant="outline"
                className="h-auto py-4 flex flex-col items-start gap-2 hover:bg-slate-50 border-2 hover:border-blue-500 transition-all"
                onClick={() => handleScenarioClick(scenario)}
                disabled={loading}
              >
                <div className="font-bold text-lg">{scenario.name}</div>
                <div className="text-xs text-muted-foreground">
                  {scenario.mode === 'fashion' ? '👗 복장 추천' : '🏠 환경 조언'}
                </div>
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 결과 표시 영역 */}
      {(loading || result) && (
        <Card className="bg-white backdrop-blur border-0" style={{ borderRadius: '1rem', boxShadow: '0 10px 40px rgba(0,0,0,0.15)' }}>
          <CardHeader>
            <CardTitle className="flex justify-between items-center">
              <span>테스트 결과: {currentScenario}</span>
              {result && (
                <Badge variant={result.keyword === 'NORMAL' ? 'secondary' : 'destructive'} className="text-lg px-3 py-1">
                  키워드: {result.keyword}
                </Badge>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent className="min-h-[100px] flex items-center justify-center">
            {loading ? (
              <div className="flex flex-col items-center gap-3 text-muted-foreground">
                <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
                <p>가상 데이터 분석 및 SenseHAT 제어 중...</p>
              </div>
            ) : (
              <div className="text-lg leading-relaxed text-slate-800 font-medium w-full">
                 {result?.text}
              </div>
            )}
          </CardContent>
        </Card>
      )}
      
      <div className="text-white text-sm text-center drop-shadow-md">
        * 이 모드는 실제 센서 값을 무시하고 강제로 설정된 값을 서버로 전송합니다. <br/>
        * 라즈베리파이 SenseHAT LED가 해당 시나리오에 맞게 변경되는지 확인하세요.
      </div>
    </div>
  );
}
