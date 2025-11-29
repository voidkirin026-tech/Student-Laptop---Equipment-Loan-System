// Equipment management functionality
document.addEventListener('DOMContentLoaded', initEquipment);

async function initEquipment() {
    loadEquipmentList();
    document.getElementById('add-equipment-form').addEventListener('submit', handleAddEquipment);
}

async function loadEquipmentList() {
    try {
        const response = await fetch('/api/equipment');
        const equipment = await response.json();
        
        const tbody = document.querySelector('#equipment-table tbody');
        const noEquipmentMsg = document.getElementById('no-equipment');
        
        tbody.innerHTML = '';
        
        if (equipment.length === 0) {
            document.getElementById('equipment-table').style.display = 'none';
            noEquipmentMsg.style.display = 'block';
            return;
        }
        
        document.getElementById('equipment-table').style.display = 'table';
        noEquipmentMsg.style.display = 'none';
        
        equipment.forEach(item => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.serial_number}</td>
                <td>${item.category}</td>
                <td><span class="status-${item.availability_status.toLowerCase()}">${item.availability_status}</span></td>
                <td>${item.condition || 'Good'}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading equipment:', error);
    }
}

async function handleAddEquipment(event) {
    event.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        serial_number: document.getElementById('serial').value,
        category: document.getElementById('category').value,
        condition: document.getElementById('condition').value,
        availability_status: 'Available'
    };
    
    try {
        const response = await fetch('/api/equipment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            alert('Equipment added successfully!');
            document.getElementById('add-equipment-form').reset();
            loadEquipmentList();
        } else {
            alert('Error adding equipment');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding equipment');
    }
}
