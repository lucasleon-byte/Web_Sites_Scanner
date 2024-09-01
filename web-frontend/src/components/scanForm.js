import React, { useState } from 'react';

const ScanForm = ({ onScan, onRescan, scannedUrl, loading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onScan(url);
  };

  const handleRescanClick = () => {
    onRescan(scannedUrl);
  };

  return (
    <div>
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
        </div>
      )}
      <form onSubmit={handleSubmit} className="scan-form">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL to scan"
          required
          disabled={loading} 
        />
        <button type="submit" className="scan-button" disabled={loading}>
          {loading ? 'Scanning...' : 'Scan'}
        </button>
        {scannedUrl && (
          <button type="button" onClick={handleRescanClick} className="rescan-button" disabled={loading}>
            {loading ? 'Rescanning...' : 'Rescan'}
          </button>
        )}
      </form>
    </div>
  );
};

export default ScanForm;
