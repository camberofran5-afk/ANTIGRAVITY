const API_URL = 'http://localhost:8000/api/v1';

export const api = {
    // Animals
    async getAnimals(ranchId: string) {
        const res = await fetch(`${API_URL}/cattle?ranch_id=${ranchId}&limit=100`);
        return res.json();
    },

    async createAnimal(data: any) {
        const res = await fetch(`${API_URL}/cattle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async updateAnimal(id: string, data: any) {
        const res = await fetch(`${API_URL}/cattle/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async deleteAnimal(id: string) {
        const res = await fetch(`${API_URL}/cattle/${id}`, {
            method: 'DELETE'
        });
        return res.json();
    },

    // Events
    async createEvent(data: any) {
        const res = await fetch(`${API_URL}/events`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async getEvents(cattleId: string) {
        const res = await fetch(`${API_URL}/events?cattle_id=${cattleId}`);
        return res.json();
    },

    async getEventsByRanch(ranchId: string) {
        const res = await fetch(`${API_URL}/events?ranch_id=${ranchId}&limit=1000`);
        return res.json();
    },

    // Inventory
    async getInventory(ranchId: string) {
        const res = await fetch(`${API_URL}/inventory?ranch_id=${ranchId}&limit=100`);
        return res.json();
    },

    async createInventoryItem(data: any) {
        const res = await fetch(`${API_URL}/inventory`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Clients
    async getClients(ranchId: string) {
        const res = await fetch(`${API_URL}/clients?ranch_id=${ranchId}&limit=100`);
        return res.json();
    },

    async createClient(data: any) {
        const res = await fetch(`${API_URL}/clients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Costs
    async getCosts(ranchId: string, startDate?: string, endDate?: string) {
        let url = `${API_URL}/costs?ranch_id=${ranchId}&limit=1000`;
        if (startDate) url += `&start_date=${startDate}`;
        if (endDate) url += `&end_date=${endDate}`;
        const res = await fetch(url);
        return res.json();
    },

    async createCost(data: any) {
        const res = await fetch(`${API_URL}/costs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },

    // Metrics
    async getMetrics(ranchId: string) {
        const res = await fetch(`${API_URL}/metrics/kpis?ranch_id=${ranchId}`);
        return res.json();
    },

    async getSummary(ranchId: string) {
        const res = await fetch(`${API_URL}/metrics/summary?ranch_id=${ranchId}`);
        return res.json();
    }
};
