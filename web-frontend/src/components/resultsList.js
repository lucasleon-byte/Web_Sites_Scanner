import React from 'react';
import { useNavigate } from 'react-router-dom';

const ResultsList = ({ results, onSelectAlertType, scannedUrl, currentTool }) => {
    const navigate = useNavigate();
    const [responseData] = Array.isArray(results) ? results : [null];
    const message = responseData?.message || results.message ;
    const newScanUrl = responseData?.new_scan_url || results.new_scan_url;
    const scanData = responseData?.scan_data?.data || {};

    const handleLinkClick = (event) => {
        event.preventDefault(); 
        const url = `/results/${scanData.id}`; 
        window.open(url, '_blank', 'noopener,noreferrer'); 
    };

    const renderResults = () => {
        if (currentTool === 'zap') {
            const alertTypes = Array.isArray(results.alert_types) ? results.alert_types : [];
            return (
                <div>
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
        } else if (currentTool === 'nmap') {
            const scanDataString = results.scan_data || '';
            const rows = scanDataString.split('\r\n').filter(row => row);
            const headers = rows[0] ? rows[0].split(';') : [];
            const dataRows = rows.slice(1).map(row => row.split(';'));

            return (
                <div>
                    {dataRows.length === 0 ? (
                        <p>No data found.</p>
                    ) : (
                        <table className="scan-results-table-nmap">
                            <thead>
                                <tr>
                                    {headers.map((header, index) => (
                                        <th key={index} className="scan-results-header-nmap">
                                            {header}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {dataRows.map((dataRow, rowIndex) => (
                                    <tr key={rowIndex} className="scan-results-row-nmap">
                                        {dataRow.map((cell, cellIndex) => (
                                            <td key={cellIndex} className="scan-results-cell-nmap">
                                                {cell}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            );
        } else if (currentTool === 'virustotal') {
            const analysisId = scanData.id || 'N/A';
            const analysisLink = scanData.links ? scanData.links.self : '#';

            return (
                <div className="virustotal-section">
                    <h3>VirusTotal Scan Data</h3>
                    <p><strong>Analysis ID:</strong> {analysisId}</p>
                    <p>
                        
                        <a href={`http://localhost:5000/results/${analysisId}`} onClick={handleLinkClick}>
                            View Results
                        </a>
                    </p>
                </div>
            );
        } else {
            return <p>Tool not supported.</p>;
        }
    };

    return (
        <div className="results-list">
            <h2>Scan Results</h2>
            {renderResults()}
            {message && (
                <div className="message">
                    <p>{message}</p>
                    {newScanUrl && <a href="#">Scan again</a>}
                </div>
            )}
        </div>
    );
};

export default ResultsList;
