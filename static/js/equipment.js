// Equipment management functionality
document.addEventListener('DOMContentLoaded', initEquipment);

let currentEditingId = null;

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
            const actionsHTML = `
                <button class="action-btn edit-btn" onclick="editEquipment('${item.id}')">✏️ Edit</button>
                <button class="action-btn delete-btn" onclick="deleteEquipment('${item.id}', '${item.name}')">🗑️ Delete</button>
            `;
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.model || '-'}</td>
                <td>${item.serial_number}</td>
                <td>${item.category}</td>
                <td><span class="status-${item.availability_status.toLowerCase()}">${item.availability_status}</span></td>
                <td>${item.condition || 'Good'}</td>
                <td>${actionsHTML}</td>
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

async function editEquipment(equipmentId) {
    try {
        // Fetch equipment details
        const response = await fetch(`/api/equipment/${equipmentId}`);
        if (!response.ok) throw new Error('Failed to fetch equipment');
        const equipment = await response.json();
        
        // Show edit prompts
        const newName = prompt('Equipment Name:', equipment.name);
        if (newName === null) return;
        
        const newModel = prompt('Model:', equipment.model || '');
        const newCondition = prompt('Condition (Excellent/Good/Fair/Poor/Damaged):', equipment.condition || 'Good');
        const newCategory = prompt('Category:', equipment.category || '');
        
        // Update equipment
        const updateResponse = await fetch(`/api/equipment/${equipmentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: newName,
                model: newModel,
                category: newCategory,
                condition: newCondition
            })
        });
        
        if (updateResponse.ok) {
            alert('Equipment updated successfully!');
            loadEquipmentList();
        } else {
            const error = await updateResponse.json();
            alert('Error updating equipment: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating equipment');
    }
}

async function deleteEquipment(equipmentId, equipmentName) {
    if (!confirm(`Are you sure you want to delete "${equipmentName}"? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/equipment/${equipmentId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Equipment deleted successfully!');
            loadEquipmentList();
        } else {
            const error = await response.json();
            alert('Error deleting equipment: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting equipment');
    }
}
