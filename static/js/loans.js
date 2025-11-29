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
            url = '/api/loans?status=active';
        } else if (filter === 'overdue') {
            url = '/api/loans/overdue';
        } else if (filter === 'returned') {
            url = '/api/loans?status=returned';
        }
        
        const response = await fetch(url);
        const loans = await response.json();
        
        const tbody = document.querySelector('#loans-table tbody');
        const noLoansMsg = document.getElementById('no-loans');
        
        tbody.innerHTML = '';
        
        if (loans.length === 0) {
            document.getElementById('loans-table').style.display = 'none';
            noLoansMsg.classList.add('show');
            return;
        }
        
        document.getElementById('loans-table').style.display = 'table';
        noLoansMsg.classList.remove('show');
        
        loans.forEach(loan => {
            const row = tbody.insertRow();
            const statusClass = loan.status === 'Overdue' ? 'status-overdue' : 
                               loan.status === 'Returned' ? 'status-returned' : 'status-active';
            
            row.innerHTML = `
                <td>${loan.student_name}</td>
                <td>${loan.equipment_name}</td>
                <td>${new Date(loan.checkout_date).toLocaleDateString()}</td>
                <td>${new Date(loan.due_date).toLocaleDateString()}</td>
                <td><span class="${statusClass}">${loan.status}</span></td>
                <td>
                    ${loan.status === 'Active' || loan.status === 'Overdue' ? 
                        `<button class="btn btn-success btn-sm" onclick="returnLoan(${loan.id})">Return</button>` : 
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
