import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

const AlertDetails = () => {
  const [rowData, setRowData] = useState([]);
  const [columnDefs] = useState([
    { headerName: "Message ID", field: "messageId", width: 150 },
    { headerName: "Alert", field: "alert", width: 200 },
    { headerName: "Alert Reference", field: "alertRef", width: 180 },
    { headerName: "Confidence", field: "confidence", width: 120 },
    { headerName: "CWE ID", field: "cweid", width: 120 },
    { headerName: "Description", field: "description", width: 400 },
    { headerName: "Solution", field: "solution", width: 300 },
    { headerName: "Evidence", field: "evidence", width: 250 },
    { headerName: "Input Vector", field: "inputVector", width: 250 },
    { headerName: "Method", field: "method", width: 100 },
    { headerName: "Name", field: "name", width: 200 },
    { headerName: "Other", field: "other", width: 300 },
    { headerName: "Param", field: "param", width: 150 },
    { headerName: "Plugin ID", field: "pluginId", width: 120 },
    { headerName: "Reference", field: "reference", width: 300 },
    { headerName: "Risk", field: "risk", width: 100 },
    { headerName: "Source ID", field: "sourceid", width: 120 },
    { headerName: "Tags", field: "tags", width: 250 },
    { headerName: "URL", field: "url", width: 300 },
    { headerName: "WASC ID", field: "wascid", width: 100 },
  ]);

  const location = useLocation();
  const navigate = useNavigate();
  const query = new URLSearchParams(location.search);
  const alertType = query.get('alertType');
  const url = query.get('url');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/alerts/${encodeURIComponent(alertType)}?url=${encodeURIComponent(url)}`);
        const data = await response.json();
        setRowData(data.details || []);
      } catch (error) {
        console.error('Error fetching alert details:', error);
      }
    };

    fetchData();
  }, [alertType, url]);

  
  const handleBackToAlerts = () => {
    navigate('/', { state: { scannedUrl: url } }); 
  };

  return (
    <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
      <h2>Details for {alertType}</h2>

      <AgGridReact 
        columnDefs={columnDefs} 
        rowData={rowData} 
        domLayout='autoHeight'  
        defaultColDef={{
          sortable: true,
          filter: true,
          resizable: true,
          wrapText: true,
          autoHeight: true
        }}
      />
    </div>
  );
};

export default AlertDetails;
