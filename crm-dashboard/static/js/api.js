/**
 * Client API - Fonctions fetch pour tous les endpoints
 */

const API_BASE = '/api';

async function fetchDeals() {
    try {
        const response = await fetch(`${API_BASE}/deals`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchDeals:', error);
        throw error;
    }
}

async function fetchKPIs() {
    try {
        const response = await fetch(`${API_BASE}/kpis`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchKPIs:', error);
        throw error;
    }
}

async function fetchSectorAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/analytics/sectors`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchSectorAnalytics:', error);
        throw error;
    }
}

async function fetchDeadlines() {
    try {
        const response = await fetch(`${API_BASE}/analytics/deadlines`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchDeadlines:', error);
        throw error;
    }
}

async function uploadCSV(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch(`${API_BASE}/upload/csv`, {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur uploadCSV:', error);
        throw error;
    }
}
