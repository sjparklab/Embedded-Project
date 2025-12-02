import { useState, useEffect } from 'react';
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
import { Switch } from './ui/switch';
import { Slider } from './ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

interface SettingsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: () => void;
}

interface City {
  id: number;
  name: string;
  name_ko: string;
}

export default function SettingsDialog({ isOpen, onClose, onSave }: SettingsDialogProps) {
  const [cities, setCities] = useState<City[]>([]);

  const [location, setLocation] = useState<string>('');
  const [temperatureUnit, setTemperatureUnit] = useState<'celsius' | 'fahrenheit'>('celsius');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState([30]);
  const [ttsEnabled, setTtsEnabled] = useState(true);
  const [ttsSpeed, setTtsSpeed] = useState([1]);
  const [ttsPitch, setTtsPitch] = useState([1]);

  // 🔥 도시 목록 가져오기
  useEffect(() => {
    fetch("/api/cities/")
      .then((res) => res.json())
      .then((data) => setCities(data))
      .catch((err) => console.error("도시 목록 로드 실패:", err));
  }, []);

  // 🔥 기존 설정 가져오기
  useEffect(() => {
    fetch("/api/settings")
      .then(res => res.json())
      .then(saved => {
        if (!saved) return;

        setLocation(saved.location || "");
        setTemperatureUnit(saved.temperatureUnit || "celsius");
        setAutoRefresh(saved.autoRefresh ?? true);
        setRefreshInterval([saved.refreshInterval || 30]);
        setTtsEnabled(saved.ttsEnabled ?? true);
        setTtsSpeed([saved.ttsSpeed || 1]);
        setTtsPitch([saved.ttsPitch || 1]);
      })
      .catch(err => console.warn("설정 로드 실패 → localStorage fallback:", err));
  }, []);

  // 🔥 저장 버튼
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
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      });

      if (!response.ok) throw new Error("설정 저장 실패");

      onSave();
      onClose();
    } catch (error) {
      console.warn("백엔드 연결 안됨 → localStorage fallback");
      localStorage.setItem("weatherAppSettings", JSON.stringify(settings));

      onSave();
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      {/* ⭐ 경고 제거 핵심: aria-describedby 추가 */}
      <DialogContent
        aria-describedby="settings-description"
        className="max-w-2xl max-h-[80vh] overflow-y-auto"
      >
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
              <SettingsIcon className="w-5 h-5 text-white" />
            </div>
            환경 설정
          </DialogTitle>

          {/* ⭐ 접근성 규칙 충족: id 추가 */}
          <DialogDescription id="settings-description">
            날씨 정보 및 패션 추천 설정을 변경할 수 있습니다.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* 🔵 위치 설정 */}
          <section className="space-y-3 p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-blue-600" />
              <Label className="text-blue-900">위치 설정</Label>
            </div>

            <Select value={location} onValueChange={setLocation}>
              <SelectTrigger className="bg-white border-blue-200">
                <SelectValue placeholder="도시 선택" />
              </SelectTrigger>
              <SelectContent>
                {cities.map(city => (
                  <SelectItem key={city.id} value={String(city.id)}>
                    {city.name_ko} ({city.name})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <p className="text-blue-700 text-sm">
              한국 주요 도시 중 하나를 선택하세요.
            </p>
          </section>

          {/* 🔴 온도 단위 */}
          <section className="space-y-3 p-4 bg-red-50 rounded-lg">
            <div className="flex items-center gap-2">
              <Thermometer className="w-5 h-5 text-red-600" />
              <Label>온도 단위</Label>
            </div>

            <Select
              value={temperatureUnit}
              onValueChange={(v: string) => setTemperatureUnit(v as "celsius" | "fahrenheit")}>
              <SelectTrigger className="bg-white border-red-200">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
               <SelectItem value="celsius">섭씨 (°C)</SelectItem>
               <SelectItem value="fahrenheit">화씨 (°F)</SelectItem>
              </SelectContent>
            </Select>
          </section>

          {/* 🟢 자동 새로고침 */}
          <section className="space-y-3 p-4 bg-green-50 rounded-lg">
            <div className="flex items-center justify-between">
              <Label className="text-green-900">자동 새로고침</Label>
              <Switch checked={autoRefresh} onCheckedChange={setAutoRefresh} />
            </div>

            {autoRefresh && (
              <div className="mt-3">
                <Label>새로고침 간격: {refreshInterval[0]}분</Label>
                <Slider
                  min={5}
                  max={60}
                  step={5}
                  value={refreshInterval}
                  onValueChange={setRefreshInterval}
                  className="mt-2"
                />
              </div>
            )}
          </section>

          {/* 🟣 음성 안내 */}
          <section className="space-y-3 p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center justify-between">
              <Label>음성 안내 (TTS)</Label>
              <Switch checked={ttsEnabled} onCheckedChange={setTtsEnabled} />
            </div>

            {ttsEnabled && (
              <div className="space-y-3 mt-3">
                <div>
                  <Label>재생 속도: {ttsSpeed[0].toFixed(1)}x</Label>
                  <Slider
                    min={0.5}
                    max={2}
                    step={0.1}
                    value={ttsSpeed}
                    onValueChange={setTtsSpeed}
                  />
                </div>

                <div>
                  <Label>음높이: {ttsPitch[0].toFixed(1)}</Label>
                  <Slider
                    min={0.5}
                    max={2}
                    step={0.1}
                    value={ttsPitch}
                    onValueChange={setTtsPitch}
                  />
                </div>
              </div>
            )}
          </section>
        </div>

        {/* 버튼 */}
        <div className="flex justify-end gap-3 pt-4 border-t">
          <Button variant="outline" onClick={onClose}>
            취소
          </Button>
          <Button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white" onClick={handleSave}>
            저장
          </Button>
        </div>

      </DialogContent>
    </Dialog>
  );
}
