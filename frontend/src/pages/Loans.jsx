import React, { useState, useEffect } from 'react';
import { loanService } from '../services/api';
import '../styles/pages.css';

export const Loans = () => {
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLoans();
  }, []);

  const fetchLoans = async () => {
    try {
      setLoading(true);
      const response = await loanService.getAll();
      setLoans(response.data);
    } catch (err) {
      setError('Failed to load loans');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page-container"><p>Loading loans...</p></div>;
  if (error) return <div className="page-container error">{error}</div>;

  return (
    <div className="page-container">
      <h1>Loan Management</h1>
      <p>Total Loans: {loans.length}</p>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Equipment</th>
              <th>Student</th>
              <th>Check-out Date</th>
              <th>Return Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loans.map((loan) => (
              <tr key={loan.id}>
                <td>{loan.equipment_name}</td>
                <td>{loan.student_name}</td>
                <td>{new Date(loan.checkout_date).toLocaleDateString()}</td>
                <td>{new Date(loan.expected_return_date).toLocaleDateString()}</td>
                <td>{loan.status}</td>
                <td>
                  <button className="btn-small">View</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
