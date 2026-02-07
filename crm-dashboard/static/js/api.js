/**
 * Client API - Fonctions fetch pour tous les endpoints
 * Supporte les filtres optionnels via query parameters
 */

const API_BASE = '/api';

function buildQueryString(filters) {
    if (!filters) return '';
    const params = new URLSearchParams();
    if (filters.statut && filters.statut.length) {
        filters.statut.forEach(s => params.append('statut', s));
    }
    if (filters.secteur && filters.secteur.length) {
        filters.secteur.forEach(s => params.append('secteur', s));
    }
    if (filters.assignee && filters.assignee.length) {
        filters.assignee.forEach(a => params.append('assignee', a));
    }
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    if (filters.search) params.append('search', filters.search);
    const qs = params.toString();
    return qs ? '?' + qs : '';
}

async function fetchDeals(filters) {
    try {
        const response = await fetch(`${API_BASE}/deals${buildQueryString(filters)}`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchDeals:', error);
        throw error;
    }
}

async function fetchKPIs(filters) {
    try {
        const response = await fetch(`${API_BASE}/kpis${buildQueryString(filters)}`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchKPIs:', error);
        throw error;
    }
}

async function fetchSectorAnalytics(filters) {
    try {
        const response = await fetch(`${API_BASE}/analytics/sectors${buildQueryString(filters)}`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchSectorAnalytics:', error);
        throw error;
    }
}

async function fetchDeadlines(filters) {
    try {
        const response = await fetch(`${API_BASE}/analytics/deadlines${buildQueryString(filters)}`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchDeadlines:', error);
        throw error;
    }
}

async function fetchPerformance(filters) {
    try {
        const response = await fetch(`${API_BASE}/analytics/performance${buildQueryString(filters)}`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchPerformance:', error);
        throw error;
    }
}

async function fetchFilterOptions() {
    try {
        const response = await fetch(`${API_BASE}/filters/options`);
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur fetchFilterOptions:', error);
        throw error;
    }
}

async function createDeal(data) {
    try {
        const response = await fetch(`${API_BASE}/deals`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur createDeal:', error);
        throw error;
    }
}

async function updateDeal(id, data) {
    try {
        const response = await fetch(`${API_BASE}/deals/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur updateDeal:', error);
        throw error;
    }
}

async function deleteDeal(id) {
    try {
        const response = await fetch(`${API_BASE}/deals/${id}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        if (!result.success) throw new Error(result.error);
        return result.data;
    } catch (error) {
        console.error('Erreur deleteDeal:', error);
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
