// Student management functionality
document.addEventListener('DOMContentLoaded', initStudents);

async function initStudents() {
    loadStudentsList();
    document.getElementById('add-student-form').addEventListener('submit', handleAddStudent);
}

async function loadStudentsList() {
    try {
        const response = await fetch('/api/students');
        if (!response.ok) throw new Error('Failed to fetch students');
        const students = await response.json();
        
        const tbody = document.querySelector('#students-table tbody');
        const noStudentsMsg = document.getElementById('no-students');
        
        tbody.innerHTML = '';
        
        if (students.length === 0) {
            document.getElementById('students-table').style.display = 'none';
            noStudentsMsg.style.display = 'block';
            return;
        }
        
        document.getElementById('students-table').style.display = 'table';
        noStudentsMsg.style.display = 'none';
        
        students.forEach(student => {
            const row = tbody.insertRow();
            const studentName = `${student.first_name} ${student.last_name}`.replace(/'/g, "\\'");
            const actionsHTML = `
                <button class="action-btn edit-btn" onclick="editStudent('${student.id}')">✏️ Edit</button>
                <button class="action-btn delete-btn" onclick="deleteStudent('${student.id}', '${studentName}')">🗑️ Delete</button>
            `;
            row.innerHTML = `
                <td>${student.first_name || '-'}</td>
                <td>${student.last_name || '-'}</td>
                <td>${student.email || '-'}</td>
                <td>${student.program || '-'}</td>
                <td>${student.year_level || '-'}</td>
                <td><span class="status-${student.status}">${student.status}</span></td>
                <td>${actionsHTML}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading students:', error);
        alert('Error loading students');
    }
}

async function handleAddStudent(event) {
    event.preventDefault();
    
    // Validate email format
    const email = document.getElementById('email').value;
    if (!email.includes('@')) {
        alert('Please enter a valid email address');
        return;
    }
    
    const formData = {
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: email,
        program: document.getElementById('program').value || null,
        year_level: document.getElementById('year_level').value ? parseInt(document.getElementById('year_level').value) : null,
        status: 'active'
    };
    
    try {
        const response = await fetch('/api/students', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            alert('Student added successfully!');
            document.getElementById('add-student-form').reset();
            loadStudentsList();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error || 'Failed to add student'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding student');
    }
}

async function editStudent(studentId) {
    try {
        // Fetch student details
        const response = await fetch(`/api/students/${studentId}`);
        if (!response.ok) throw new Error('Failed to fetch student');
        const student = await response.json();
        
        // Show edit prompts
        const newFirstName = prompt('First Name:', student.first_name || '');
        if (newFirstName === null) return;
        
        const newLastName = prompt('Last Name:', student.last_name || '');
        if (newLastName === null) return;
        
        const newEmail = prompt('Email:', student.email || '');
        if (newEmail === null) return;
        
        const newProgram = prompt('Program:', student.program || '');
        const newYearLevel = prompt('Year Level (7-9: Junior High, 10-12: Senior High, 1-4: College):', student.year_level || '');
        
        // Validate inputs
        if (!newFirstName.trim()) {
            alert('First name cannot be empty');
            return;
        }
        if (!newLastName.trim()) {
            alert('Last name cannot be empty');
            return;
        }
        if (!newEmail.includes('@')) {
            alert('Please enter a valid email address');
            return;
        }
        if (newYearLevel && newYearLevel.trim()) {
            const yearLevelNum = parseInt(newYearLevel);
            if (!((7 <= yearLevelNum && yearLevelNum <= 12) || (1 <= yearLevelNum && yearLevelNum <= 4))) {
                alert('Invalid year level. Use 7-9 (Junior High), 10-12 (Senior High), or 1-4 (College)');
                return;
            }
        }
        
        // Update student
        const updateResponse = await fetch(`/api/students/${studentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                first_name: newFirstName.trim(),
                last_name: newLastName.trim(),
                email: newEmail.trim(),
                program: newProgram.trim() || null,
                year_level: newYearLevel ? parseInt(newYearLevel) : null
            })
        });
        
        if (updateResponse.ok) {
            alert('Student updated successfully!');
            loadStudentsList();
        } else {
            const error = await updateResponse.json();
            alert('Error updating student: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating student');
    }
}

async function deleteStudent(studentId, studentName) {
    if (!confirm(`Are you sure you want to delete "${studentName}"? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Student deleted successfully!');
            loadStudentsList();
        } else {
            const error = await response.json();
            alert('Error deleting student: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting student');
    }
}
