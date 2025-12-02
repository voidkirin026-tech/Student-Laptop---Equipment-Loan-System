import React from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/dashboard.css';

export const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user?.full_name || user?.email}!</h1>
        <p>Manage your laptop and equipment loans</p>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h2>📊 Quick Stats</h2>
          <div className="stats-placeholder">
            <p>Active Loans: Loading...</p>
            <p>Available Equipment: Loading...</p>
            <p>Pending Reservations: Loading...</p>
          </div>
        </div>

        <div className="dashboard-card">
          <h2>📝 Recent Activity</h2>
          <div className="activity-placeholder">
            <p>No recent activity</p>
          </div>
        </div>

        <div className="dashboard-card">
          <h2>⚠️ Alerts</h2>
          <div className="alerts-placeholder">
            <p>No alerts at this time</p>
          </div>
        </div>

        <div className="dashboard-card">
          <h2>🔗 Quick Links</h2>
          <ul className="quick-links">
            <li><a href="/equipment">Browse Equipment</a></li>
            <li><a href="/loans">View Loans</a></li>
            <li><a href="/reservations">Make Reservation</a></li>
            <li><a href="/reports">View Reports</a></li>
          </ul>
        </div>
      </div>
    </div>
  );
};
