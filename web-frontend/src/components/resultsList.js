import React from 'react';
import { Link } from 'react-router-dom';

const ResultsList = ({ results, onSelectAlertType, scannedUrl }) => {
    console.log("poruka",results)
    const alertTypes = Array.isArray(results.alert_types) ? results.alert_types: [];
  const message = results.message || '';
  const newScanUrl = results.new_scan_url || '';
  
  return (
    <div className="results-list">
      <h2>Scan Results</h2>
    
      {message && (
        <div className="message">
          <p>{message}</p>

        </div>
      )}
      
      {alertTypes.length === 0 ? (
        <p>No alerts found.</p>
      ) : (
        <ul>
          {alertTypes.map((alertType, index) => (
            <li key={index}>
              <button onClick={() => onSelectAlertType(alertType, scannedUrl)}>
                {alertType}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ResultsList;
