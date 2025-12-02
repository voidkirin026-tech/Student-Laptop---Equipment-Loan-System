import React, { useState, useEffect } from 'react';
import { equipmentService } from '../services/api';
import '../styles/pages.css';

export const Equipment = () => {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchEquipment();
  }, []);

  const fetchEquipment = async () => {
    try {
      setLoading(true);
      const response = await equipmentService.getAll();
      setEquipment(response.data);
    } catch (err) {
      setError('Failed to load equipment');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page-container"><p>Loading equipment...</p></div>;
  if (error) return <div className="page-container error">{error}</div>;

  return (
    <div className="page-container">
      <h1>Equipment Management</h1>
      <p>Total Equipment: {equipment.length}</p>
      
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {equipment.map((item) => (
              <tr key={item.id}>
                <td>{item.name}</td>
                <td>{item.category}</td>
                <td>{item.status}</td>
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
