/**
 * Main.js - Initialisation du dashboard et chargement des données
 */

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

async function loadKPIs() {
    try {
        const data = await fetchKPIs();

        document.getElementById('kpi-pipeline').textContent = data.pipeline_pondere_formatted;
        document.getElementById('kpi-panier').textContent = data.panier_moyen_formatted;
        document.getElementById('kpi-nb-deals').textContent = data.nombre_deals;
        document.getElementById('kpi-gagnes').textContent = data.deals_gagnes;
        document.getElementById('kpi-taux').textContent = `Taux de conversion : ${data.taux_conversion}%`;
    } catch (error) {
        console.error('Erreur loadKPIs:', error);
    }
}

async function loadDeadlines() {
    try {
        const data = await fetchDeadlines();

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

async function refreshDashboard() {
    await Promise.all([
        loadKPIs(),
        initSectorCharts(),
        loadDeadlines()
    ]);
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', refreshDashboard);
