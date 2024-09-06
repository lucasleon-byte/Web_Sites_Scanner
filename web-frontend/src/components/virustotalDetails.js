import React, { useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { useParams } from 'react-router-dom';
import './virusTotal.css'; // Ensure your CSS file is imported

const ResultsPage = () => {
    const { analysisId } = useParams();
    const [rowData, setRowData] = useState([]);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const response = await fetch(`http://localhost:5000/analysis/${analysisId}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setRowData(formatResultsData(data));
            } catch (error) {
                console.error('Error fetching analysis details:', error);
            }
        };

        fetchResults();
    }, [analysisId]);

    const formatResultsData = (data) => {
        return Object.values(data.data.attributes.results || {}).map(item => ({
            category: item.category,
            engine_name: item.engine_name,
            method: item.method,
            result: item.result
        }));
    };

    return (
        <div className="results-page">
            <div className="ag-theme-alpine" style={{ height: '100%', width: '100%' }}>
                <AgGridReact
                    rowData={rowData}
                    columnDefs={[
                        { headerName: "Category", field: "category", flex: 1 },
                        { headerName: "Engine Name", field: "engine_name", flex: 1 },
                        { headerName: "Method", field: "method", flex: 1 },
                        { headerName: "Result", field: "result", flex: 1 }
                    ]}
                    domLayout='autoHeight'
                />
            </div>
        </div>
    );
};

export default ResultsPage;
