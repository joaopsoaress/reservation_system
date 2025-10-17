// frontend/script.js
class ReservationSystem {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8000';
        this.init();
    }

    // Generic method to make API requests
    async makeRequest(endpoint, options = {}) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
            }

            return await response.json();
            
        } catch (error) {
            console.error('Request error:', error);
            throw error;
        }
    }

    // Load and display all slots
    async loadSlots() {
        this.showLoading();
        this.hideError();

        try {
            const slots = await this.makeRequest('/slots');
            this.displaySlots(slots);
            
        } catch (error) {
            this.showError(`Failed to load slots: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    // Create a new slot
    async createSlot() {
        const form = document.getElementById('createSlotForm');
        const button = form.querySelector('button[type="submit"]');
        const originalText = button.textContent;

        try {
            button.disabled = true;
            button.textContent = 'Creating...';

            const date = document.getElementById('date').value;
            const hour = document.getElementById('hour').value;
            const duration = parseInt(document.getElementById('duration').value);

            if (!date || !hour) {
                throw new Error('Date and time are required');
            }

            const slotData = {
                date: date,
                hour: hour + ':00',
                duration: duration
            };

            await this.makeRequest('/slots', {
                method: 'POST',
                body: JSON.stringify(slotData)
            });

            this.showSuccess('Slot created successfully!');
            form.reset();
            this.loadSlots();

        } catch (error) {
            this.showError(`Error creating slot: ${error.message}`);
        } finally {
            button.disabled = false;
            button.textContent = originalText;
        }
    }

    // Reserve a slot
    async reserveSlot(slotId) {
        try {
            await this.makeRequest(`/slots/${slotId}/reserve`, {
                method: 'PUT'
            });

            this.showSuccess('Slot reserved successfully!');
            this.loadSlots();

        } catch (error) {
            this.showError(`Error reserving slot: ${error.message}`);
        }
    }

    // Delete a slot
    async deleteSlot(slotId) {
        if (!confirm('Are you sure you want to delete this slot?')) {
            return;
        }

        try {
            await this.makeRequest(`/slots/${slotId}`, {
                method: 'DELETE'
            });

            this.showSuccess('Slot deleted successfully!');
            this.loadSlots();

        } catch (error) {
            this.showError(`Error deleting slot: ${error.message}`);
        }
    }

    // Display slots in the UI
    displaySlots(slots) {
        const container = document.getElementById('slotsContainer');
        const noSlots = document.getElementById('noSlots');

        if (slots.length === 0) {
            container.innerHTML = '';
            noSlots.style.display = 'block';
            return;
        }

        noSlots.style.display = 'none';
        
        container.innerHTML = slots.map(slot => `
            <div class="slot-card ${slot.status}">
                <div class="slot-info">
                    <div class="slot-date">
                        ${this.formatDate(slot.date)}
                    </div>
                    <div class="slot-time">
                        ⏰ ${this.formatTime(slot.hour)} - Duration: ${slot.duration} min
                    </div>
                    <div class="slot-duration">
                        Status: <span class="slot-status status-${slot.status}">${slot.status === 'available' ? 'Available' : 'Reserved'}</span>
                    </div>
                </div>
                <div class="slot-actions">
                    ${slot.status === 'available' ? 
                        `<button class="btn btn-success" onclick="reservationSystem.reserveSlot(${slot.id})">
                            ✅ Reserve
                        </button>` : 
                        '<span class="btn btn-secondary" disabled>🔒 Reserved</span>'
                    }
                    <button class="btn btn-danger" onclick="reservationSystem.deleteSlot(${slot.id})">
                        🗑️ Delete
                    </button>
                </div>
            </div>
        `).join('');
    }

    // Format date to a readable string
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    // Format time to a readable string
    formatTime(timeString) {
        const [hours, minutes] = timeString.split(':');
        return `${hours}:${minutes}`;
    }

    // Show loading indicator
    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('slotsContainer').style.display = 'none';
    }

    // Hide loading indicator
    hideLoading() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('slotsContainer').style.display = 'grid';
    }

    // Show error message
    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => this.hideError(), 5000);
    }

    // Hide error message
    hideError() {
        document.getElementById('errorMessage').style.display = 'none';
    }

    // Show success message
    showSuccess(message) {
        alert('✅ ' + message);
    }

    // Bind UI events
    bindEvents() {
        // Creation form
        document.getElementById('createSlotForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createSlot();
        });

        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadSlots();
        });
    }

    // Initialize the reservation system
    init() {
        this.bindEvents();
        this.loadSlots();
    }
}

// Initialize the system when the page loads
let reservationSystem;
document.addEventListener('DOMContentLoaded', () => {
    reservationSystem = new ReservationSystem();
});