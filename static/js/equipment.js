// Equipment management functionality
document.addEventListener('DOMContentLoaded', initEquipment);

let currentEditingId = null;
let currentPage = 1;
let currentFilters = {
    query: '',
    category: '',
    condition: '',
    status: ''
};

async function initEquipment() {
    loadEquipmentList();
    loadFilterOptions();
    setupEventListeners();
    document.getElementById('add-equipment-form').addEventListener('submit', handleAddEquipment);
}

function setupEventListeners() {
    // Search functionality
    document.getElementById('search-btn').addEventListener('click', performSearch);
    document.getElementById('clear-search-btn').addEventListener('click', clearSearch);
    document.getElementById('search-query').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
    
    // Filter functionality
    document.getElementById('filter-category').addEventListener('change', performSearch);
    document.getElementById('filter-condition').addEventListener('change', performSearch);
    document.getElementById('filter-status').addEventListener('change', performSearch);
}

async function loadFilterOptions() {
    try {
        // Load categories
        const categoriesResponse = await fetch('/api/filters/categories');
        if (categoriesResponse.ok) {
            const categories = await categoriesResponse.json();
            const categorySelect = document.getElementById('filter-category');
            categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                categorySelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading filter options:', error);
    }
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

async function loadEquipmentList(page = 1) {
    try {
        // Build query string
        let url = '/api/equipment?page=' + page + '&per_page=10';
        
        // Use search endpoint if any filters are active
        if (currentFilters.query || currentFilters.category || currentFilters.condition || currentFilters.status) {
            url = '/api/search/equipment?page=' + page + '&per_page=10';
            if (currentFilters.query) url += '&q=' + encodeURIComponent(currentFilters.query);
            if (currentFilters.category) url += '&category=' + encodeURIComponent(currentFilters.category);
            if (currentFilters.condition) url += '&condition=' + encodeURIComponent(currentFilters.condition);
            if (currentFilters.status) url += '&status=' + encodeURIComponent(currentFilters.status);
        }
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch equipment');
        
        const data = await response.json();
        const equipment = data.items || data;
        const totalPages = data.pages || 1;
        const total = data.total || equipment.length;
        
        const tbody = document.querySelector('#equipment-table tbody');
        const noEquipmentMsg = document.getElementById('no-equipment');
        
        tbody.innerHTML = '';
        
        if (equipment.length === 0) {
            document.getElementById('equipment-table').style.display = 'none';
            noEquipmentMsg.style.display = 'block';
            updatePaginationControls(0, 0, 0);
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
        
        updatePaginationControls(page, totalPages, total);
    } catch (error) {
        console.error('Error loading equipment:', error);
    }
}

function updatePaginationControls(currentPage, totalPages, total) {
    const topPagination = document.getElementById('pagination-top');
    const bottomPagination = document.getElementById('pagination-bottom');
    
    let html = '';
    
    if (totalPages > 1) {
        html = `
            <div class="pagination">
                <button ${currentPage === 1 ? 'disabled' : ''} onclick="loadEquipmentList(1)">First</button>
                <button ${currentPage === 1 ? 'disabled' : ''} onclick="loadEquipmentList(${currentPage - 1})">Previous</button>
        `;
        
        // Show page numbers
        for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
            html += `<button ${i === currentPage ? 'class="active"' : ''} onclick="loadEquipmentList(${i})">${i}</button>`;
        }
        
        html += `
                <button ${currentPage === totalPages ? 'disabled' : ''} onclick="loadEquipmentList(${currentPage + 1})">Next</button>
                <button ${currentPage === totalPages ? 'disabled' : ''} onclick="loadEquipmentList(${totalPages})">Last</button>
                <span class="page-info">Page ${currentPage} of ${totalPages} (${total} total)</span>
            </div>
        `;
    }
    
    topPagination.innerHTML = html;
    bottomPagination.innerHTML = html;
}

function performSearch() {
    currentFilters.query = document.getElementById('search-query').value;
    currentFilters.category = document.getElementById('filter-category').value;
    currentFilters.condition = document.getElementById('filter-condition').value;
    currentFilters.status = document.getElementById('filter-status').value;
    currentPage = 1;
    loadEquipmentList(1);
}

function clearSearch() {
    document.getElementById('search-query').value = '';
    document.getElementById('filter-category').value = '';
    document.getElementById('filter-condition').value = '';
    document.getElementById('filter-status').value = '';
    currentFilters = { query: '', category: '', condition: '', status: '' };
    currentPage = 1;
    loadEquipmentList(1);
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
