import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Hotspot, UserLocation, UserPreferences } from '../types';

interface AppState {
  // Dark mode
  darkMode: boolean;
  toggleDarkMode: () => void;

  // Hotspots
  hotspots: Hotspot[];
  setHotspots: (hotspots: Hotspot[]) => void;
  filteredHotspots: Hotspot[];
  setFilteredHotspots: (hotspots: Hotspot[]) => void;

  // User location
  userLocation: UserLocation | null;
  setUserLocation: (location: UserLocation | null) => void;

  // Filters
  severityFilter: string[];
  setSeverityFilter: (severity: string[]) => void;
  crimeTypeFilter: string[];
  setCrimeTypeFilter: (types: string[]) => void;
  timeFilter: string;
  setTimeFilter: (filter: string) => void;

  // User preferences
  preferences: UserPreferences | null;
  setPreferences: (preferences: UserPreferences) => void;

  // Loading states
  loading: boolean;
  setLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      // Dark mode
      darkMode: false,
      toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),

      // Hotspots
      hotspots: [],
      setHotspots: (hotspots) => {
        console.log('Setting hotspots:', hotspots.length);
        set((state) => {
          let filtered = [...hotspots];

          // Apply severity filter
          if (state.severityFilter && state.severityFilter.length > 0) {
            filtered = filtered.filter((h) => state.severityFilter.includes(h.severity));
          }

          // Apply crime type filter if any
          if (state.crimeTypeFilter && state.crimeTypeFilter.length > 0) {
            filtered = filtered.filter((h) => {
              const explanation = (h.explanation || '').toLowerCase();
              return state.crimeTypeFilter.some((type) => explanation.includes(type.toLowerCase()));
            });
          }

          console.log('Filtered hotspots:', filtered.length);
          return { hotspots, filteredHotspots: filtered };
        });
      },
      filteredHotspots: [],
      setFilteredHotspots: (hotspots) => set({ filteredHotspots: hotspots }),

      // User location
      userLocation: null,
      setUserLocation: (location) => set({ userLocation: location }),

      // Filters
      severityFilter: ['High', 'Medium', 'Low'],
      setSeverityFilter: (severity) => {
        set((state) => {
          const newSeverity = severity;
          let filtered = [...state.hotspots];

          // Apply severity filter
          if (newSeverity && newSeverity.length > 0) {
            filtered = filtered.filter((h) => newSeverity.includes(h.severity));
          }

          // Apply crime type filter if any
          if (state.crimeTypeFilter && state.crimeTypeFilter.length > 0) {
            filtered = filtered.filter((h) => {
              const explanation = (h.explanation || '').toLowerCase();
              return state.crimeTypeFilter.some((type) => explanation.includes(type.toLowerCase()));
            });
          }

          return { severityFilter: newSeverity, filteredHotspots: filtered };
        });
      },
      crimeTypeFilter: [],
      setCrimeTypeFilter: (types) => {
        set((state) => {
          let filtered = [...state.hotspots];

          // Apply severity filter
          if (state.severityFilter && state.severityFilter.length > 0) {
            filtered = filtered.filter((h) => state.severityFilter.includes(h.severity));
          }

          // Apply crime type filter
          if (types && types.length > 0) {
            filtered = filtered.filter((h) => {
              const explanation = (h.explanation || '').toLowerCase();
              return types.some((type) => explanation.includes(type.toLowerCase()));
            });
          }

          return { crimeTypeFilter: types, filteredHotspots: filtered };
        });
      },
      timeFilter: 'All Day',
      setTimeFilter: (filter) => set({ timeFilter: filter }),

      // User preferences
      preferences: null,
      setPreferences: (preferences) => set({ preferences }),

      // Loading states
      loading: false,
      setLoading: (loading) => set({ loading }),
      error: null,
      setError: (error) => set({ error }),
    }),
    {
      name: 'nashville-safe-tourist-storage',
      partialize: (state) => ({
        darkMode: state.darkMode,
        preferences: state.preferences,
        severityFilter: state.severityFilter,
      }),
    }
  )
);

