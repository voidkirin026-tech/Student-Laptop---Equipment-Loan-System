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
        const students = await response.json();
        
        const select = document.getElementById('student');
        students.forEach(student => {
            const option = document.createElement('option');
            option.value = student.id;
            option.textContent = student.name;
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
        const equipment = await response.json();
        
        const select = document.getElementById('equipment');
        equipment.forEach(item => {
            if (item.status === 'Available') {
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
    
    const formData = {
        student_id: parseInt(document.getElementById('student').value),
        equipment_id: parseInt(document.getElementById('equipment').value),
        due_date: document.getElementById('due-date').value,
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
