import React, { useState, useEffect } from 'react';
import { reservationService } from '../services/api';
import '../styles/pages.css';

export const Reservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchReservations();
  }, []);

  const fetchReservations = async () => {
    try {
      setLoading(true);
      const response = await reservationService.getAll();
      setReservations(response.data);
    } catch (err) {
      setError('Failed to load reservations');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page-container"><p>Loading reservations...</p></div>;
  if (error) return <div className="page-container error">{error}</div>;

  return (
    <div className="page-container">
      <h1>Reservation Management</h1>
      <p>Total Reservations: {reservations.length}</p>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Equipment</th>
              <th>Student</th>
              <th>Reservation Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {reservations.map((reservation) => (
              <tr key={reservation.id}>
                <td>{reservation.equipment_name}</td>
                <td>{reservation.student_name}</td>
                <td>{new Date(reservation.reservation_date).toLocaleDateString()}</td>
                <td>{reservation.status}</td>
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
