import { useState } from 'react';
import { MapPin, Thermometer, Volume2, RefreshCw, Settings as SettingsIcon } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { Switch } from './ui/switch';
import { Slider } from './ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

interface SettingsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: () => void;
}

export default function SettingsDialog({ isOpen, onClose, onSave }: SettingsDialogProps) {
  const [location, setLocation] = useState('서울');
  const [temperatureUnit, setTemperatureUnit] = useState('celsius');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState([30]);
  const [ttsEnabled, setTtsEnabled] = useState(true);
  const [ttsSpeed, setTtsSpeed] = useState([1]);
  const [ttsPitch, setTtsPitch] = useState([1]);

  const handleSave = async () => {
    const settings = {
      location,
      temperatureUnit,
      autoRefresh,
      refreshInterval: refreshInterval[0],
      ttsEnabled,
      ttsSpeed: ttsSpeed[0],
      ttsPitch: ttsPitch[0],
    };

    try {
      // ============================================
      // Flask 백엔드 API 엔드포인트: /api/settings
      // 사용자 설정을 저장합니다
      // ============================================
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });

      if (!response.ok) {
        throw new Error('설정 저장에 실패했습니다');
      }

      // 설정 저장 후 데이터 새로고침
      onSave();
      onClose();
    } catch (error) {
      console.error('설정 저장 에러:', error);
      
      // ============================================
      // 개발 환경: localStorage에 설정 저장
      // 통합시에 백엔드 API 연결 해야함.
      // ============================================
      localStorage.setItem('weatherAppSettings', JSON.stringify(settings));
      
      // 설정 저장 후 데이터 새로고침
      onSave();
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
              <SettingsIcon className="w-5 h-5 text-white" />
            </div>
            환경 설정
          </DialogTitle>
          <DialogDescription>
            날씨 정보 및 패션 추천 설정을 변경할 수 있습니다.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* 위치 설정 */}
          <div className="space-y-3 p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-blue-600" />
              <Label className="text-blue-900">위치 설정</Label>
            </div>
            <Input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="도시 이름을 입력하세요 (예: 서울, 부산)"
              className="bg-white border-blue-200"
            />
            <p className="text-blue-700 text-sm">
              날씨 정보를 가져올 위치를 설정합니다. 변경 후 저장하면 새로운 위치의 날씨 정보가 표시됩니다.
            </p>
          </div>

          {/* 온도 단위 */}
          <div className="space-y-3 p-4 bg-red-50 rounded-lg">
            <div className="flex items-center gap-2">
              <Thermometer className="w-5 h-5 text-red-600" />
              <Label className="text-red-900">온도 단위</Label>
            </div>
            <Select value={temperatureUnit} onValueChange={setTemperatureUnit}>
              <SelectTrigger className="bg-white border-red-200">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="celsius">섭씨 (°C)</SelectItem>
                <SelectItem value="fahrenheit">화씨 (°F)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* 자동 새로고침 */}
          <div className="space-y-3 p-4 bg-green-50 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <RefreshCw className="w-5 h-5 text-green-600" />
                <Label className="text-green-900">자동 새로고침</Label>
              </div>
              <Switch
                checked={autoRefresh}
                onCheckedChange={setAutoRefresh}
              />
            </div>
            <p className="text-green-700 text-sm">
              설정한 간격마다 자동으로 날씨 정보를 업데이트합니다.
            </p>
            {autoRefresh && (
              <div className="space-y-2 mt-4">
                <div className="flex justify-between">
                  <Label className="text-green-900">새로고침 간격</Label>
                  <span className="text-green-700 font-medium">{refreshInterval[0]}분</span>
                </div>
                <Slider
                  value={refreshInterval}
                  onValueChange={setRefreshInterval}
                  min={5}
                  max={60}
                  step={5}
                  className="w-full"
                />
              </div>
            )}
          </div>

          {/* TTS 설정 */}
          <div className="space-y-3 p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Volume2 className="w-5 h-5 text-purple-600" />
                <Label className="text-purple-900">음성 안내 (TTS)</Label>
              </div>
              <Switch
                checked={ttsEnabled}
                onCheckedChange={setTtsEnabled}
              />
            </div>
            <p className="text-purple-700 text-sm">
              패션 추천 내용을 음성으로 들을 수 있습니다.
            </p>

            {ttsEnabled && (
              <div className="space-y-4 mt-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label className="text-purple-900">재생 속도</Label>
                    <span className="text-purple-700 font-medium">{ttsSpeed[0].toFixed(1)}x</span>
                  </div>
                  <Slider
                    value={ttsSpeed}
                    onValueChange={setTtsSpeed}
                    min={0.5}
                    max={2}
                    step={0.1}
                    className="w-full"
                  />
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between">
                    <Label className="text-purple-900">음높이</Label>
                    <span className="text-purple-700 font-medium">{ttsPitch[0].toFixed(1)}</span>
                  </div>
                  <Slider
                    value={ttsPitch}
                    onValueChange={setTtsPitch}
                    min={0.5}
                    max={2}
                    step={0.1}
                    className="w-full"
                  />
                </div>
              </div>
            )}
          </div>

          {/* API 설정 안내 */}
          <div className="space-y-3 p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🔑</span>
              <h3 className="font-semibold text-gray-900">백엔드 API 설정 안내</h3>
            </div>
            <div className="space-y-2">
              <p className="text-gray-700">
                Flask 백엔드에서 다음 API 엔드포인트를 구현해야 합니다:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-1 ml-2">
                <li><code className="bg-gray-200 px-2 py-1 rounded text-sm">GET /api/weather</code> - 날씨 데이터 가져오기</li>
                <li><code className="bg-gray-200 px-2 py-1 rounded text-sm">POST /api/fashion-recommendation</code> - 패션 추천 가져오기</li>
                <li><code className="bg-gray-200 px-2 py-1 rounded text-sm">POST /api/settings</code> - 설정 저장하기</li>
              </ul>
              <p className="text-gray-700 mt-3">
                필요한 환경 변수:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-1 ml-2">
                <li><code className="bg-gray-200 px-2 py-1 rounded text-sm">OPENWEATHER_API_KEY</code></li>
                <li><code className="bg-gray-200 px-2 py-1 rounded text-sm">OPENAI_API_KEY</code></li>
              </ul>
            </div>
          </div>
        </div>

        {/* 액션 버튼 */}
        <div className="flex justify-end gap-3 pt-4 border-t">
          <Button variant="outline" onClick={onClose}>
            취소
          </Button>
          <Button 
            onClick={handleSave} 
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white"
          >
            저장
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
