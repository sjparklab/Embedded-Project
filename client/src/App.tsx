import { useState, useEffect } from 'react';
import { Settings, RefreshCw } from 'lucide-react';
import { Button } from './components/ui/button';
import WeatherCard from './components/WeatherCard';
import FashionRecommendation from './components/FashionRecommendation';
import EnvironmentRecommendation from './components/EnvironmentRecommendation';
import SettingsDialog from './components/SettingsDialog';

// 타입 정의
interface WeatherData {
  temperature: number;
  humidity: number;
  pressure: number;
  co2: number;
  weather: string;
  description: string;
  location: string;
}

interface RecommendationData {
  text: string;
}

interface UserSettings {
  location: string;
  temperatureUnit: string;
  autoRefresh: boolean;
  refreshInterval: number;
  ttsEnabled: boolean;
  ttsSpeed: number;
  ttsPitch: number;
}

export default function App() {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);

  const [fashionRecommendation, setFashionRecommendation] =
    useState<RecommendationData | null>(null);
  const [environmentRecommendation, setEnvironmentRecommendation] =
    useState<RecommendationData | null>(null);

  const [isWeatherLoading, setIsWeatherLoading] = useState(true);
  const [isFashionLoading, setIsFashionLoading] = useState(true);
  const [isEnvironmentLoading, setIsEnvironmentLoading] = useState(true);

  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const [settings, setSettings] = useState<UserSettings | null>(null);

  // ---------------------------
  // 0) settings 불러오기
  // ---------------------------
  const loadSettings = async () => {
    try {
      const res = await fetch("/api/settings");
      const json = await res.json();
      setSettings(json);
    } catch (err) {
      console.warn("설정 로드 실패 → localStorage fallback");

      const local = localStorage.getItem("weatherAppSettings");
      if (local) setSettings(JSON.parse(local));
    }
  };

  // ---------------------------
  // 1) 날씨 불러오기
  // ---------------------------
  const fetchWeather = async () => {
    if (!settings) return;

    setIsWeatherLoading(true);

    try {
      // ******* 🔥 여기만 수정됨 🔥 *******
      const res = await fetch(`/api/weather/dashboard`);
      // ***********************************

      const json = await res.json();
      setWeatherData(json);
      setLastUpdated(new Date());
    } catch (err) {
      console.error("날씨 데이터 로드 실패:", err);

      setWeatherData({
        temperature: 18,
        humidity: 60,
        pressure: 1013,
        co2: 420,
        weather: "Clear",
        description: "clear sky",
        location: "Fallback City",
      });
    } finally {
      setIsWeatherLoading(false);
    }
  };

  // ---------------------------
  // 2) 패션 추천
  // ---------------------------
  const fetchFashionRecommendation = async (weather: WeatherData) => {
    setIsFashionLoading(true);

    try {
      const res = await fetch("/api/gpt/fashion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(weather),
      });

      const json = await res.json();
      setFashionRecommendation(json);
    } catch (err) {
      console.error("패션 추천 불러오기 실패:", err);

      setFashionRecommendation({
        text: "AI 추천 생성 실패. 기본 패션 추천을 표시합니다."
      });
    } finally {
      setIsFashionLoading(false);
    }
  };

  // ---------------------------
  // 3) 환경 조언
  // ---------------------------
  const fetchEnvironmentRecommendation = async (weather: WeatherData) => {
    setIsEnvironmentLoading(true);

    try {
      const res = await fetch("/api/gpt/environment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(weather),
      });

      const json = await res.json();
      setEnvironmentRecommendation(json);
    } catch (err) {
      console.error("환경 조언 불러오기 실패:", err);

      setEnvironmentRecommendation({
        text: "AI 조언 생성 실패. 기본 환경 조언을 표시합니다."
      });
    } finally {
      setIsEnvironmentLoading(false);
    }
  };

  // ---------------------------
  // 마운트 시 설정 먼저 로드
  // ---------------------------
  useEffect(() => {
    loadSettings();
  }, []);

  // ---------------------------
  // settings 로드 후 날씨 요청
  // ---------------------------
  useEffect(() => {
    if (settings) {
      fetchWeather();
    }
  }, [settings]);

  // ---------------------------
  // 날씨 → 패션 · 환경 조언 요청
  // ---------------------------
  useEffect(() => {
    if (weatherData) {
      fetchFashionRecommendation(weatherData);
      fetchEnvironmentRecommendation(weatherData);
    }
  }, [weatherData]);

  const handleRefresh = async () => {
    await fetchWeather();
  };

  const handleSettingsSaved = async () => {
    await loadSettings();
    await fetchWeather();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-400 via-blue-500 to-indigo-600 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">

        {/* 헤더 */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-white drop-shadow-lg">
              5조 ChatGPT 기반 스마트 생활 조언 시스템
            </h1>

            {lastUpdated && (
              <p className="text-white/80 text-sm mt-1">
                마지막 업데이트: {lastUpdated.toLocaleTimeString("ko-KR")}
              </p>
            )}
          </div>

          <div className="flex gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleRefresh}
              className="rounded-full bg-white/20 hover:bg-white/30 text-white backdrop-blur-sm"
            >
              <RefreshCw className="w-5 h-5" />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsSettingsOpen(true)}
              className="rounded-full bg-white/20 hover:bg-white/30 text-white backdrop-blur-sm"
            >
              <Settings className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* ============================= */}
        {/* 🚀 새 레이아웃 시작 */}
        {/* ============================= */}
        <div className="grid grid-cols-1 gap-6">

          {/* 대시보드 전체 */}
          <div>
            {settings && (
              <WeatherCard
                data={weatherData}
                isLoading={isWeatherLoading}
                unit={settings.temperatureUnit as "celsius" | "fahrenheit"}
              />
            )}
          </div>

          {/* 두 번째 줄: 패션 + 환경 추천 */}
          <div className="grid grid-cols-2 gap-6">
            <FashionRecommendation
              recommendation={fashionRecommendation}
              isLoading={isFashionLoading}
            />

            <EnvironmentRecommendation
              recommendation={environmentRecommendation}
              isLoading={isEnvironmentLoading}
            />
          </div>
        </div>
        {/* ============================= */}
        {/* 🚀 새 레이아웃 끝 */}
        {/* ============================= */}

      </div>

      <SettingsDialog
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSave={handleSettingsSaved}
      />
    </div>
  );
}
