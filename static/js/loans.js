// Loans management functionality
document.addEventListener('DOMContentLoaded', initLoans);

let currentFilter = 'all';
let currentLoanId = null;
let currentLoanData = null;

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
    
    // Damage form submission
    document.getElementById('damage-form').addEventListener('submit', handleDamageSubmit);
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
        if (!response.ok) throw new Error('Failed to fetch loans');
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

function returnLoan(loanId) {
    try {
        // Fetch loan details to show damage assessment
        fetch(`/api/loans/${loanId}`)
            .then(r => r.json())
            .then(loan => {
                currentLoanId = loanId;
                currentLoanData = loan;
                openDamageModal(loan);
            });
    } catch (error) {
        console.error('Error:', error);
        alert('Error fetching loan details');
    }
}

function openDamageModal(loan) {
    const modal = document.getElementById('damage-modal');
    modal.style.display = 'block';
    
    // Calculate days late if overdue
    if (loan.status === 'Overdue' || loan.date_due) {
        const dueDate = new Date(loan.date_due);
        const today = new Date();
        const daysLate = Math.max(0, Math.floor((today - dueDate) / (1000 * 60 * 60 * 24)));
        
        if (daysLate > 0) {
            document.getElementById('charge-summary').style.display = 'block';
            document.getElementById('days-late').textContent = daysLate;
            document.getElementById('late-fee').textContent = (daysLate * 5).toFixed(2);
        }
    }
}

function closeDamageModal() {
    const modal = document.getElementById('damage-modal');
    modal.style.display = 'none';
    document.getElementById('damage-form').reset();
    document.getElementById('charge-summary').style.display = 'none';
    currentLoanId = null;
    currentLoanData = null;
}

async function handleDamageSubmit(event) {
    event.preventDefault();
    
    if (!currentLoanId) {
        alert('Error: No loan selected');
        return;
    }
    
    const damageStatus = document.getElementById('damage-status').value;
    const damageNotes = document.getElementById('damage-notes').value;
    const newCondition = document.getElementById('new-condition').value;
    
    if (!newCondition) {
        alert('Please select a condition');
        return;
    }
    
    try {
        const response = await fetch(`/api/loans/${currentLoanId}/return-with-damage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                damage_status: damageStatus,
                damage_notes: damageNotes,
                new_condition: newCondition
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            let message = 'Equipment returned successfully!';
            
            if (result.late_fine > 0) {
                message += `\n\nLate Return Charges:\n`;
                message += `Days Late: ${result.days_late}\n`;
                message += `Charge (₱5/day): ₱${result.late_fine.toFixed(2)}`;
            }
            
            if (damageStatus !== 'None') {
                message += `\n\nDamage Assessment:\nStatus: ${damageStatus}`;
                if (damageNotes) {
                    message += `\nNotes: ${damageNotes}`;
                }
            }
            
            alert(message);
            closeDamageModal();
            loadLoans(currentFilter);
        } else {
            const error = await response.json();
            alert('Error returning equipment: ' + (error.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error returning equipment');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('damage-modal');
    if (event.target === modal) {
        closeDamageModal();
    }
}
