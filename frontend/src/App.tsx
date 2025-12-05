import { Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import { useStore } from './store/useStore';
import Layout from './components/Layout';
import MapView from './pages/MapView';
import RoutePlanner from './pages/RoutePlanner';
import Statistics from './pages/Statistics';
import SafetyCalculator from './pages/SafetyCalculator';
import Trends from './pages/Trends';
import Settings from './pages/Settings';

function App() {
  const { darkMode, setError, setLoading, setHotspots } = useStore();

  useEffect(() => {
    // Apply dark mode class to document
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  useEffect(() => {
    // Load hotspots on mount
    const loadHotspots = async () => {
      setLoading(true);
      try {
        const { getHotspots } = await import('./services/api');
        const hotspots = await getHotspots();
        setHotspots(hotspots);
        setError(null);
      } catch (error) {
        console.error('Failed to load hotspots:', error);
        setError('Failed to load hotspot data. Please check if the backend server is running.');
      } finally {
        setLoading(false);
      }
    };

    loadHotspots();
  }, [setHotspots, setError, setLoading]);

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<MapView />} />
        <Route path="/route-planner" element={<RoutePlanner />} />
        <Route path="/statistics" element={<Statistics />} />
        <Route path="/safety-calculator" element={<SafetyCalculator />} />
        <Route path="/trends" element={<Trends />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  );
}

export default App;

