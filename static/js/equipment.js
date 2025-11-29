// Equipment management functionality
document.addEventListener('DOMContentLoaded', initEquipment);

async function initEquipment() {
    loadEquipmentList();
    document.getElementById('add-equipment-form').addEventListener('submit', handleAddEquipment);
}

function updateCategory() {
    const select = document.getElementById('category-select');
    const input = document.getElementById('category');
    
    if (select.value && select.value !== 'Other') {
        input.value = select.value;
    } else {
        input.value = '';
        input.focus();
    }
}

async function loadEquipmentList() {
    try {
        const response = await fetch('/api/equipment');
        if (!response.ok) throw new Error('Failed to fetch equipment');
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
                <td>${item.model || '-'}</td>
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
    
    const conditionSelect = document.getElementById('condition').value;
    if (!conditionSelect) {
        alert('Please select a condition for the equipment');
        return;
    }
    
    const formData = {
        name: document.getElementById('name').value,
        model: document.getElementById('model').value,
        serial_number: document.getElementById('serial').value,
        category: document.getElementById('category').value,
        condition: conditionSelect,
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
