// Checkout form functionality
document.addEventListener('DOMContentLoaded', initCheckout);

async function initCheckout() {
    // Load students
    loadStudents();
    // Load available equipment
    loadEquipment();
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('due-date').min = today;
    
    // Form submission
    document.getElementById('checkout-form').addEventListener('submit', handleCheckout);
}

async function loadStudents() {
    try {
        const response = await fetch('/api/students');
        if (!response.ok) throw new Error('Failed to fetch students');
        const students = await response.json();
        
        const select = document.getElementById('student');
        students.forEach(student => {
            const option = document.createElement('option');
            option.value = student.id;
            option.textContent = `${student.first_name} ${student.last_name}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading students:', error);
        showMessage('Error loading students', 'danger');
    }
}

async function loadEquipment() {
    try {
        const response = await fetch('/api/equipment');
        if (!response.ok) throw new Error('Failed to fetch equipment');
        const equipment = await response.json();
        
        const select = document.getElementById('equipment');
        equipment.forEach(item => {
            if (item.availability_status === 'Available') {
                const option = document.createElement('option');
                option.value = item.id;
                option.textContent = `${item.name} (${item.serial_number})`;
                select.appendChild(option);
            }
        });
    } catch (error) {
        console.error('Error loading equipment:', error);
        showMessage('Error loading equipment', 'danger');
    }
}

async function handleCheckout(event) {
    event.preventDefault();
    
    const studentId = document.getElementById('student').value;
    const equipmentId = document.getElementById('equipment').value;
    const dueDate = document.getElementById('due-date').value;
    
    // Validate that all fields are selected
    if (!studentId || !equipmentId || !dueDate) {
        showMessage('Please select all required fields', 'danger');
        return;
    }
    
    // Validate that due date is in the future
    const dueDateObj = new Date(dueDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (dueDateObj < today) {
        showMessage('Due date must be in the future', 'danger');
        return;
    }
    
    const formData = {
        student_id: studentId,
        equipment_id: equipmentId,
        due_date: dueDate,
        notes: document.getElementById('notes').value
    };
    
    try {
        const response = await fetch('/api/loans/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Equipment checked out successfully!', 'success');
            document.getElementById('checkout-form').reset();
            setTimeout(() => loadEquipment(), 1000);
        } else {
            showMessage(result.error || 'Error during checkout', 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error during checkout', 'danger');
    }
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.innerHTML = '';
        }, 5000);
    }
}
