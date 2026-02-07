/**
 * Main.js - Initialisation du dashboard et chargement des données
 */

// Filtres actifs globaux
let currentFilters = null;

function formatMontant(value) {
    return new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }).format(value) + ' \u20AC';
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;
        return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    } catch {
        return dateStr;
    }
}

const STATUT_BADGES = {
    'prospect': 'bg-blue-100 text-blue-800',
    'qualifié': 'bg-yellow-100 text-yellow-800',
    'négociation': 'bg-orange-100 text-orange-800',
    'gagné': 'bg-green-100 text-green-800',
    'gagné - en cours': 'bg-green-100 text-green-800'
};

function getStatutBadge(statut) {
    const key = (statut || '').toLowerCase().trim();
    const classes = STATUT_BADGES[key] || 'bg-gray-100 text-gray-800';
    return `<span class="statut-badge px-2 py-0.5 rounded-full text-xs font-medium ${classes}">${statut}</span>`;
}

async function loadKPIs(filters) {
    try {
        const data = await fetchKPIs(filters);
        document.getElementById('kpi-pipeline').textContent = data.pipeline_pondere_formatted;
        document.getElementById('kpi-panier').textContent = data.panier_moyen_formatted;
        document.getElementById('kpi-nb-deals').textContent = data.nombre_deals;
        document.getElementById('kpi-gagnes').textContent = data.deals_gagnes;
        document.getElementById('kpi-taux').textContent = `Taux de conversion : ${data.taux_conversion}%`;
    } catch (error) {
        console.error('Erreur loadKPIs:', error);
    }
}

async function loadDealsTable(filters) {
    try {
        const deals = await fetchDeals(filters);
        const tbody = document.getElementById('table-deals');

        if (!deals || deals.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="px-4 py-4 text-gray-400 text-center">Aucun deal. Importez un CSV ou créez un deal manuellement.</td></tr>';
            return;
        }

        tbody.innerHTML = deals.map(d => `
            <tr class="border-b border-gray-100 hover:bg-gray-50">
                <td class="px-4 py-3 font-medium text-gray-800">${d.client || '-'}</td>
                <td class="px-4 py-3">${getStatutBadge(d.statut)}</td>
                <td class="px-4 py-3">${formatMontant(d.montant_brut)}</td>
                <td class="px-4 py-3 text-gray-600">${d.secteur || '-'}</td>
                <td class="px-4 py-3 text-gray-600">${d.assignee || '-'}</td>
                <td class="px-4 py-3">${formatDate(d.date_echeance)}</td>
                <td class="px-4 py-3">
                    <div class="flex gap-2">
                        <button class="btn-edit text-blue-600 hover:text-blue-800 text-xs font-medium" data-deal='${JSON.stringify(d).replace(/'/g, "&#39;")}'>Modifier</button>
                        <button class="btn-delete text-red-600 hover:text-red-800 text-xs font-medium" data-id="${d.id}" data-client="${(d.client || '').replace(/"/g, '&quot;')}" data-montant="${d.montant_brut}">Supprimer</button>
                    </div>
                </td>
            </tr>
        `).join('');

        // Attach event listeners
        tbody.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', function() {
                const deal = JSON.parse(this.dataset.deal);
                openDealModal('edit', deal);
            });
        });

        tbody.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.dataset.id;
                const client = this.dataset.client;
                const montant = this.dataset.montant;
                handleDeleteDeal(id, client, montant);
            });
        });

    } catch (error) {
        console.error('Erreur loadDealsTable:', error);
    }
}

async function loadDeadlines(filters) {
    try {
        const data = await fetchDeadlines(filters);

        // Alerte retards
        const alert = document.getElementById('alert-overdue');
        const alertText = document.getElementById('alert-overdue-text');
        if (data.stats.nb_overdue > 0) {
            alertText.textContent = `${data.stats.nb_overdue} deal(s) en retard !`;
            alert.classList.remove('hidden');
        } else {
            alert.classList.add('hidden');
        }

        // Tableau échéances dépassées
        const tbodyOverdue = document.getElementById('table-overdue');
        if (data.overdue.length === 0) {
            tbodyOverdue.innerHTML = '<tr><td colspan="4" class="px-5 py-4 text-gray-400 text-center">Aucun deal en retard</td></tr>';
        } else {
            tbodyOverdue.innerHTML = data.overdue.map(d => `
                <tr class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="px-5 py-3 font-medium text-gray-800">${d.client}</td>
                    <td class="px-5 py-3">${d.montant_formatted}</td>
                    <td class="px-5 py-3">${formatDate(d.date_echeance)}</td>
                    <td class="px-5 py-3 text-red-600 font-medium">${d.jours_retard}j</td>
                </tr>
            `).join('');
        }

        // Tableau échéances à venir
        const tbodyUpcoming = document.getElementById('table-upcoming');
        if (data.upcoming.length === 0) {
            tbodyUpcoming.innerHTML = '<tr><td colspan="4" class="px-5 py-4 text-gray-400 text-center">Aucun deal dans les 30 prochains jours</td></tr>';
        } else {
            tbodyUpcoming.innerHTML = data.upcoming.map(d => `
                <tr class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="px-5 py-3 font-medium text-gray-800">${d.client}</td>
                    <td class="px-5 py-3">${d.montant_formatted}</td>
                    <td class="px-5 py-3">${formatDate(d.date_echeance)}</td>
                    <td class="px-5 py-3 text-green-600 font-medium">${d.jours_restants}j</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Erreur loadDeadlines:', error);
    }
}

async function refreshDashboard(filters) {
    currentFilters = filters || null;
    await Promise.all([
        loadKPIs(filters),
        loadDealsTable(filters),
        initSectorCharts(filters),
        initPerformanceChart(filters),
        loadDeadlines(filters)
    ]);
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Restaurer les filtres depuis localStorage
    const savedFilters = localStorage.getItem('crm_filters');
    const filters = savedFilters ? JSON.parse(savedFilters) : null;
    currentFilters = filters;
    refreshDashboard(filters);
});
