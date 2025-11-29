// Loans management functionality
document.addEventListener('DOMContentLoaded', initLoans);

let currentFilter = 'all';

async function initLoans() {
    loadLoans('all');
    
    // Filter button listeners
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            loadLoans(currentFilter);
        });
    });
}

async function loadLoans(filter) {
    try {
        let url = '/api/loans';
        if (filter === 'active') {
            url = '/api/loans/active';
        } else if (filter === 'overdue') {
            url = '/api/loans/overdue';
        }
        
        const response = await fetch(url);
        const loans = await response.json();
        
        // Filter returned loans locally if needed
        let filteredLoans = loans;
        if (filter === 'returned') {
            filteredLoans = loans.filter(l => l.status === 'Returned');
        }
        
        const tbody = document.querySelector('#loans-table tbody');
        const noLoansMsg = document.getElementById('no-loans');
        
        tbody.innerHTML = '';
        
        if (filteredLoans.length === 0) {
            document.getElementById('loans-table').style.display = 'none';
            noLoansMsg.classList.add('show');
            return;
        }
        
        document.getElementById('loans-table').style.display = 'table';
        noLoansMsg.classList.remove('show');
        
        filteredLoans.forEach(loan => {
            const row = tbody.insertRow();
            const studentName = loan.student ? `${loan.student.first_name} ${loan.student.last_name}` : 'Unknown';
            const equipmentName = loan.equipment ? loan.equipment.name : 'Unknown';
            const statusClass = loan.status === 'Overdue' ? 'status-overdue' : 
                               loan.status === 'Returned' ? 'status-returned' : 'status-active';
            
            row.innerHTML = `
                <td>${studentName}</td>
                <td>${equipmentName}</td>
                <td>${loan.date_borrowed ? new Date(loan.date_borrowed).toLocaleDateString() : 'N/A'}</td>
                <td>${loan.date_due ? new Date(loan.date_due).toLocaleDateString() : 'N/A'}</td>
                <td><span class="${statusClass}">${loan.status}</span></td>
                <td>
                    ${loan.status === 'Borrowed' ? 
                        `<button class="btn btn-success btn-sm" onclick="returnLoan('${loan.id}')">Return</button>` : 
                        '-'}
                </td>
            `;
        });
    } catch (error) {
        console.error('Error loading loans:', error);
    }
}

async function returnLoan(loanId) {
    if (!confirm('Are you sure you want to return this equipment?')) return;
    
    try {
        const response = await fetch(`/api/loans/${loanId}/return`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Equipment returned successfully!');
            loadLoans(currentFilter);
        } else {
            alert('Error returning equipment');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error returning equipment');
    }
}
