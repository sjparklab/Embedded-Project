import { useState, useEffect } from 'react';
import { Settings, RefreshCw } from 'lucide-react';
import { Button } from './components/ui/button';
import WeatherCard from './components/WeatherCard';
import FashionRecommendation from './components/FashionRecommendation';
import SettingsDialog from './components/SettingsDialog';

// Flask 백엔드로부터 받을 데이터 타입 정의
interface WeatherData {
  temperature: number;
  humidity: number;
  pressure: number;
  co2: number;
  weather: string;
  description: string;
  location: string;
}

interface FashionRecommendationData {
  text: string;
}

export default function App() {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [fashionRecommendation, setFashionRecommendation] = useState<FashionRecommendationData | null>(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // Flask 백엔드에서 데이터를 가져오는 함수
  const fetchData = async () => {
    setIsLoading(true);
    
    // ============================================
    // Flask 백엔드가 준비되지 않은 경우 Mock 데이터 사용
    // 백엔드가 준비되면 USE_MOCK_DATA를 false로 변경
    // ============================================
    const USE_MOCK_DATA = true;
    
    if (USE_MOCK_DATA) {
      // Mock 데이터를 사용하여 개발 환경에서 테스트
      setTimeout(() => {
        const mockWeatherData: WeatherData = {
          temperature: 18,
          humidity: 65,
          pressure: 1013,
          co2: 420,
          weather: '맑음',
          description: '화창한 날씨',
          location: '서울'
        };
        setWeatherData(mockWeatherData);

        const mockFashionRecommendation: FashionRecommendationData = {
          text: '오늘은 기온이 18도로 쾌적한 날씨입니다. 가볍게 입을 수 있는 긴팔 티셔츠에 얇은 자켓을 걸치는 것을 추천합니다. 습도가 65%로 적당하니 면 소재의 옷이 좋겠습니다. 날씨가 맑으니 선글라스를 챙기시는 것도 좋겠어요!'
        };
        setFashionRecommendation(mockFashionRecommendation);
        
        setLastUpdated(new Date());
        setIsLoading(false);
      }, 800);
      return;
    }
    
    try {
      // ============================================
      // Flask 백엔드 API 엔드포인트: /api/weather
      // OpenWeather API를 통해 날씨 데이터를 가져옵니다
      // ============================================
      const weatherResponse = await fetch('/api/weather', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      // Content-Type이 JSON인지 확인
      const contentType = weatherResponse.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('서버가 JSON 형식의 응답을 반환하지 않았습니다');
      }
      
      if (!weatherResponse.ok) {
        throw new Error(`날씨 데이터를 가져오는데 실패했습니다 (상태 코드: ${weatherResponse.status})`);
      }
      
      const weatherData: WeatherData = await weatherResponse.json();
      setWeatherData(weatherData);

      // ============================================
      // Flask 백엔드 API 엔드포인트: /api/fashion-recommendation
      // ChatGPT API를 통해 패션 추천을 가져옵니다
      // 날씨 데이터를 기반으로 추천을 생성합니다
      // ============================================
      const fashionResponse = await fetch('/api/fashion-recommendation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(weatherData),
      });

      // Content-Type이 JSON인지 확인
      const fashionContentType = fashionResponse.headers.get('content-type');
      if (!fashionContentType || !fashionContentType.includes('application/json')) {
        throw new Error('서버가 JSON 형식의 응답을 반환하지 않았습니다');
      }

      if (!fashionResponse.ok) {
        throw new Error(`패션 추천 데이터를 가져오는데 실패했습니다 (상태 코드: ${fashionResponse.status})`);
      }

      const fashionData: FashionRecommendationData = await fashionResponse.json();
      setFashionRecommendation(fashionData);

      setLastUpdated(new Date());
    } catch (error) {
      console.error('데이터 로드 에러:', error);
      
      // ============================================
      // 에러 발생 시 Fallback Mock 데이터 사용
      // 백엔드 연결 실패 시에도 UI가 동작하도록 합니다
      // ============================================
      const mockWeatherData: WeatherData = {
        temperature: 18,
        humidity: 65,
        pressure: 1013,
        co2: 420,
        weather: '맑음',
        description: '화창한 날씨',
        location: '서울'
      };
      setWeatherData(mockWeatherData);

      const mockFashionRecommendation: FashionRecommendationData = {
        text: '오늘은 기온이 18도로 쾌적한 날씨입니다. 가볍게 입을 수 있는 긴팔 티셔츠에 얇은 자켓을 걸치는 것을 추천합니다. 습도가 65%로 적당하니 면 소재의 옷이 좋겠습니다. 날씨가 맑으니 선글라스를 챙기시는 것도 좋겠어요!'
      };
      setFashionRecommendation(mockFashionRecommendation);
      
      setLastUpdated(new Date());
    } finally {
      setIsLoading(false);
    }
  };

  // 컴포넌트 마운트 시 데이터 로드
  useEffect(() => {
    fetchData();
  }, []);

  // 새로고침 핸들러
  const handleRefresh = () => {
    fetchData();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-400 via-blue-500 to-indigo-600 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-white drop-shadow-lg">5조-ChatGPT 기반 스마트 생활 조언 시스템</h1>
            {lastUpdated && (
              <p className="text-white/80 text-sm mt-1">
                마지막 업데이트: {lastUpdated.toLocaleTimeString('ko-KR')}
              </p>
            )}
          </div>
          <div className="flex gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleRefresh}
              disabled={isLoading}
              className="rounded-full bg-white/20 hover:bg-white/30 text-white backdrop-blur-sm"
            >
              <RefreshCw className={`w-5 h-5 ${isLoading ? 'animate-spin' : ''}`} />
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

        {/* 메인 콘텐츠 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 날씨 정보 카드 - 2/3 너비 */}
          <div className="lg:col-span-2">
            <WeatherCard data={weatherData} isLoading={isLoading} />
          </div>

          {/* 패션 추천 섹션 - 1/3 너비 */}
          <div className="lg:col-span-1">
            <FashionRecommendation 
              recommendation={fashionRecommendation} 
              isLoading={isLoading}
            />
          </div>
        </div>
      </div>

      {/* 환경설정 다이얼로그 */}
      <SettingsDialog 
        isOpen={isSettingsOpen} 
        onClose={() => setIsSettingsOpen(false)}
        onSave={fetchData}
      />
    </div>
  );
}
