import { Thermometer, Droplets, Gauge, Wind, MapPin, Sun, Cloud, CloudRain, CloudSnow } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Skeleton } from './ui/skeleton';

interface WeatherData {
  temperature: number;
  humidity: number;
  pressure: number;
  co2: number;
  weather: string;
  description: string;
  location: string;
}

interface WeatherCardProps {
  data: WeatherData | null;
  isLoading: boolean;
}

// 날씨 상태에 따른 아이콘 반환
const getWeatherIcon = (weather: string) => {
  const weatherLower = weather.toLowerCase();
  
  if (weatherLower.includes('맑음') || weatherLower.includes('clear')) {
    return <Sun className="w-20 h-20 text-yellow-400" />;
  } else if (weatherLower.includes('비') || weatherLower.includes('rain')) {
    return <CloudRain className="w-20 h-20 text-blue-300" />;
  } else if (weatherLower.includes('눈') || weatherLower.includes('snow')) {
    return <CloudSnow className="w-20 h-20 text-blue-200" />;
  } else {
    return <Cloud className="w-20 h-20 text-gray-300" />;
  }
};

export default function WeatherCard({ data, isLoading }: WeatherCardProps) {
  if (isLoading) {
    return (
      <Card className="shadow-2xl border-0 bg-white/90 backdrop-blur-md overflow-hidden">
        <CardContent className="p-8">
          <div className="space-y-6">
            <div className="flex justify-between items-start">
              <div className="space-y-2">
                <Skeleton className="h-8 w-32" />
                <Skeleton className="h-12 w-24" />
              </div>
              <Skeleton className="h-20 w-20 rounded-full" />
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="space-y-2">
                  <Skeleton className="h-4 w-16" />
                  <Skeleton className="h-8 w-20" />
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!data) return null;

  const weatherDetails = [
    {
      icon: <Droplets className="w-5 h-5 text-blue-500" />,
      label: '습도',
      value: `${data.humidity}%`,
    },
    {
      icon: <Gauge className="w-5 h-5 text-purple-500" />,
      label: '기압',
      value: `${data.pressure} hPa`,
    },
    {
      icon: <Wind className="w-5 h-5 text-green-500" />,
      label: 'CO₂',
      value: `${data.co2} ppm`,
    },
  ];

  return (
    <Card className="shadow-2xl border-0 bg-white/90 backdrop-blur-md overflow-hidden hover:shadow-3xl transition-shadow">
      <CardContent className="p-8">
        {/* 메인 날씨 정보 */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <MapPin className="w-5 h-5 text-gray-600" />
              <h2 className="text-gray-700">{data.location}</h2>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-6xl font-bold text-gray-900">{data.temperature}°</span>
              <span className="text-2xl text-gray-600">C</span>
            </div>
            <p className="text-gray-600 mt-2 text-lg">{data.description}</p>
          </div>
          <div className="flex flex-col items-center gap-2">
            {getWeatherIcon(data.weather)}
            <span className="text-gray-700 font-medium">{data.weather}</span>
          </div>
        </div>

        {/* 상세 날씨 정보 */}
        <div className="grid grid-cols-3 gap-6 pt-6 border-t border-gray-200">
          {weatherDetails.map((item, index) => (
            <div 
              key={index} 
              className="flex flex-col gap-2"
            >
              <div className="flex items-center gap-2 text-gray-500">
                {item.icon}
                <span className="text-sm">{item.label}</span>
              </div>
              <p className="text-xl font-semibold text-gray-900">
                {item.value}
              </p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
