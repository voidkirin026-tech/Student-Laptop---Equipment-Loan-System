// Dashboard functionality
document.addEventListener('DOMContentLoaded', loadDashboard);

async function loadDashboard() {
    try {
        // Load equipment stats
        const equipResponse = await fetch('/api/equipment');
        const equipment = await equipResponse.json();
        
        document.getElementById('total-equipment').textContent = equipment.length;
        document.getElementById('available-equipment').textContent = equipment.filter(e => e.status === 'Available').length;
        
        // Load loans stats
        const loansResponse = await fetch('/api/loans');
        const loans = await loansResponse.json();
        
        document.getElementById('active-loans').textContent = loans.filter(l => l.status === 'Active').length;
        
        // Load overdue loans
        const overdueResponse = await fetch('/api/loans/overdue');
        const overdue = await overdueResponse.json();
        
        document.getElementById('overdue-count').textContent = overdue.length;
        
        loadOverdueTable(overdue);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function loadOverdueTable(overdueLoans) {
    const tbody = document.querySelector('#overdue-table tbody');
    const noOverdueMsg = document.getElementById('no-overdue');
    
    tbody.innerHTML = '';
    
    if (overdueLoans.length === 0) {
        document.getElementById('overdue-table').style.display = 'none';
        noOverdueMsg.style.display = 'block';
        return;
    }
    
    document.getElementById('overdue-table').style.display = 'table';
    noOverdueMsg.style.display = 'none';
    
    overdueLoans.forEach(loan => {
        const row = tbody.insertRow();
        const daysOverdue = Math.floor((new Date() - new Date(loan.due_date)) / (1000 * 60 * 60 * 24));
        
        row.innerHTML = `
            <td>${loan.student_name}</td>
            <td>${loan.equipment_name}</td>
            <td>${new Date(loan.due_date).toLocaleDateString()}</td>
            <td>${daysOverdue} days</td>
            <td>
                <button class="btn btn-success btn-sm" onclick="returnEquipment(${loan.id})">Return</button>
            </td>
        `;
    });
}

async function returnEquipment(loanId) {
    if (!confirm('Are you sure you want to mark this as returned?')) return;
    
    try {
        const response = await fetch(`/api/loans/${loanId}/return`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Equipment returned successfully');
            loadDashboard();
        } else {
            alert('Error returning equipment');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error returning equipment');
    }
}

// Refresh dashboard every 30 seconds
setInterval(loadDashboard, 30000);
