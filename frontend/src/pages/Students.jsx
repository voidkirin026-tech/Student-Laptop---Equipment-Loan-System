import React, { useState, useEffect } from 'react';
import { studentService } from '../services/api';
import '../styles/pages.css';

export const Students = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const response = await studentService.getAll();
      setStudents(response.data);
    } catch (err) {
      setError('Failed to load students');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="page-container"><p>Loading students...</p></div>;
  if (error) return <div className="page-container error">{error}</div>;

  return (
    <div className="page-container">
      <h1>Student Management</h1>
      <p>Total Students: {students.length}</p>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Student ID</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {students.map((student) => (
              <tr key={student.id}>
                <td>{student.full_name}</td>
                <td>{student.student_id}</td>
                <td>{student.email}</td>
                <td>{student.phone}</td>
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
