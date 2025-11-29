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
            row.innerHTML = `
                <td>${student.first_name || '-'}</td>
                <td>${student.last_name || '-'}</td>
                <td>${student.email || '-'}</td>
                <td>${student.program || '-'}</td>
                <td>${student.year_level || '-'}</td>
                <td><span class="status-${student.status}">${student.status}</span></td>
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
