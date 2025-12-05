import { useStore } from '../store/useStore';
import { Filter, X } from 'lucide-react';
import { useState } from 'react';

export default function FilterPanel() {
  const {
    severityFilter,
    setSeverityFilter,
    crimeTypeFilter,
    setCrimeTypeFilter,
    timeFilter,
    setTimeFilter,
    hotspots,
    filteredHotspots,
  } = useStore();

  const [isOpen, setIsOpen] = useState(false);

  const severityOptions = ['High', 'Medium', 'Low'];
  const timeOptions = ['All Day', 'Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-22)', 'Night (22-6)', 'Current Time'];

  return (
    <>
      {/* Filter Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="filter-button fixed bottom-6 right-6 bg-primary-600 hover:bg-primary-700 text-white p-4 rounded-full shadow-lg flex items-center space-x-2 transition-all duration-200"
        aria-label="Open filters"
      >
        <Filter className="w-5 h-5" />
        <span className="hidden sm:inline">Filters</span>
        {filteredHotspots.length !== hotspots.length && hotspots.length > 0 && (
          <span className="bg-danger-500 text-white text-xs rounded-full px-2 py-1">
            {filteredHotspots.length}/{hotspots.length}
          </span>
        )}
      </button>

      {/* Filter Panel */}
      {isOpen && (
        <>
          {/* Overlay */}
          <div
            className="filter-panel-overlay fixed inset-0 bg-black bg-opacity-50"
            onClick={() => setIsOpen(false)}
          />

          {/* Panel */}
          <div
            className="filter-panel fixed right-0 top-0 h-full w-80 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 shadow-2xl overflow-y-auto"
          >
            <div className="p-6">
              {/* Header */}
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">🔍 Filter Hotspots</h2>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                  aria-label="Close filters"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Severity Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Show only (Risk Level):
                </label>
                <div className="space-y-2">
                  {severityOptions.map((severity) => (
                    <label key={severity} className="flex items-center space-x-2 cursor-pointer group">
                      <input
                        type="checkbox"
                        checked={severityFilter.includes(severity)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSeverityFilter([...severityFilter, severity]);
                          } else {
                            setSeverityFilter(severityFilter.filter((s) => s !== severity));
                          }
                        }}
                        className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300 group-hover:text-primary-600 dark:group-hover:text-primary-400">
                        {severity}
                      </span>
                      {severity === 'High' && <span className="text-danger-500">●</span>}
                      {severity === 'Medium' && <span className="text-warning-500">●</span>}
                      {severity === 'Low' && <span className="text-success-500">●</span>}
                    </label>
                  ))}
                </div>
              </div>

              {/* Time Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Time-Based Filter:
                </label>
                <select
                  value={timeFilter}
                  onChange={(e) => setTimeFilter(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                >
                  {timeOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
                {timeFilter !== 'All Day' && (
                  <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                    💡 Risk levels adjusted for {timeFilter}
                  </p>
                )}
              </div>

              {/* Stats */}
              <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Showing <strong className="text-gray-900 dark:text-white">{filteredHotspots.length}</strong> of{' '}
                  <strong className="text-gray-900 dark:text-white">{hotspots.length}</strong> hotspots
                </p>
                {filteredHotspots.length === 0 && hotspots.length > 0 && (
                  <p className="text-xs text-warning-600 dark:text-warning-400 mt-2">
                    ⚠️ All hotspots filtered out. Adjust filters to see results.
                  </p>
                )}
              </div>

              {/* Reset Button */}
              <button
                onClick={() => {
                  setSeverityFilter(['High', 'Medium', 'Low']);
                  setCrimeTypeFilter([]);
                  setTimeFilter('All Day');
                }}
                className="w-full mt-4 px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg transition-colors duration-200 font-medium"
              >
                Reset All Filters
              </button>
            </div>
          </div>
        </>
      )}
    </>
  );
}
