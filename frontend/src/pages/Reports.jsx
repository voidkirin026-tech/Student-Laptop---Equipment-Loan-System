import React, { useState, useEffect } from 'react';
import { reportService } from '../services/api';
import '../styles/pages.css';

export const Reports = () => {
  const [activeTab, setActiveTab] = useState('equipment');
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchReport = async (reportType) => {
    try {
      setLoading(true);
      setError('');
      let response;

      switch (reportType) {
        case 'equipment':
          response = await reportService.getEquipmentStatus();
          break;
        case 'loans':
          response = await reportService.getLoanActivity();
          break;
        case 'overdue':
          response = await reportService.getOverdueAnalysis();
          break;
        case 'damage':
          response = await reportService.getDamageAnalysis();
          break;
        case 'students':
          response = await reportService.getStudentActivity();
          break;
        default:
          return;
      }

      setReportData(response.data);
    } catch (err) {
      setError('Failed to load report');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport(activeTab);
  }, [activeTab]);

  return (
    <div className="page-container">
      <h1>Reports & Analytics</h1>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'equipment' ? 'active' : ''}`}
          onClick={() => setActiveTab('equipment')}
        >
          Equipment Status
        </button>
        <button
          className={`tab ${activeTab === 'loans' ? 'active' : ''}`}
          onClick={() => setActiveTab('loans')}
        >
          Loan Activity
        </button>
        <button
          className={`tab ${activeTab === 'overdue' ? 'active' : ''}`}
          onClick={() => setActiveTab('overdue')}
        >
          Overdue Analysis
        </button>
        <button
          className={`tab ${activeTab === 'damage' ? 'active' : ''}`}
          onClick={() => setActiveTab('damage')}
        >
          Damage Analysis
        </button>
        <button
          className={`tab ${activeTab === 'students' ? 'active' : ''}`}
          onClick={() => setActiveTab('students')}
        >
          Student Activity
        </button>
      </div>

      <div className="report-content">
        {loading && <p>Loading report...</p>}
        {error && <div className="error">{error}</div>}
        {reportData && (
          <pre>{JSON.stringify(reportData, null, 2)}</pre>
        )}
      </div>
    </div>
  );
};
