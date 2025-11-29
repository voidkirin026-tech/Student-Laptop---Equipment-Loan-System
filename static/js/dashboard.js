// Dashboard functionality
document.addEventListener('DOMContentLoaded', loadDashboard);

async function loadDashboard() {
    try {
        // Load equipment stats
        const equipResponse = await fetch('/api/equipment');
        if (!equipResponse.ok) throw new Error('Failed to fetch equipment');
        const equipment = await equipResponse.json();
        
        document.getElementById('total-equipment').textContent = (equipment && equipment.length) || 0;
        document.getElementById('available-equipment').textContent = (equipment && equipment.filter(e => e.availability_status === 'Available').length) || 0;
        
        // Load loans stats
        const loansResponse = await fetch('/api/loans');
        if (!loansResponse.ok) throw new Error('Failed to fetch loans');
        const loans = await loansResponse.json();
        
        document.getElementById('active-loans').textContent = (loans && loans.filter(l => l.status === 'Borrowed').length) || 0;
        
        // Load overdue loans
        const overdueResponse = await fetch('/api/loans/overdue');
        if (!overdueResponse.ok) throw new Error('Failed to fetch overdue loans');
        const overdue = await overdueResponse.json();
        
        document.getElementById('overdue-count').textContent = (overdue && overdue.length) || 0;
        
        loadOverdueTable(overdue || []);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        // Set defaults if error occurs
        document.getElementById('total-equipment').textContent = '0';
        document.getElementById('available-equipment').textContent = '0';
        document.getElementById('active-loans').textContent = '0';
        document.getElementById('overdue-count').textContent = '0';
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
        const daysOverdue = Math.floor((new Date() - new Date(loan.date_due)) / (1000 * 60 * 60 * 24));
        const studentName = loan.student ? `${loan.student.first_name} ${loan.student.last_name}` : 'Unknown';
        const equipmentName = loan.equipment ? loan.equipment.name : 'Unknown';
        
        row.innerHTML = `
            <td>${equipmentName}</td>
            <td>${studentName}</td>
            <td>${new Date(loan.date_due).toLocaleDateString()}</td>
            <td>${daysOverdue} days</td>
            <td>
                <button class="btn btn-success btn-sm" onclick="returnEquipment('${loan.id}')">Return</button>
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
