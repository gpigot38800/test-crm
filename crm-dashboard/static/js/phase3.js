/**
 * Phase 3 V2 - Vitesse de Vente, Simulateur What-If, Deals Froids
 */

let velocityChart = null;

// Données KPIs stockées pour le simulateur What-If
let kpiData = null;

/**
 * Vitesse de Vente - Chargement et affichage
 */
async function loadVelocity(filters) {
    try {
        const data = await fetchVelocity(filters);

        // KPI vitesse moyenne
        const kpiEl = document.getElementById('kpi-velocity');
        kpiEl.textContent = data.vitesse_moyenne_formatted || 'N/A';

        // Éléments du layout
        const chartWrapper = document.getElementById('velocity-chart-wrapper');
        const emptyState = document.getElementById('velocity-empty-state');
        const contentGrid = document.getElementById('velocity-content');
        const canvas = document.getElementById('chart-velocity');
        const sectors = data.velocity_by_sector || {};
        const labels = Object.keys(sectors);
        const values = Object.values(sectors);

        // Vérifier si au moins une valeur > 0 pour afficher le graphique
        const hasChartData = labels.length > 0 && values.some(v => v > 0);

        // Si pas de données utiles pour le graphique
        if (!hasChartData) {
            chartWrapper.classList.add('hidden');
            contentGrid.classList.remove('md:grid-cols-2');
            if (data.has_won_deals || labels.length > 0) {
                emptyState.classList.remove('hidden');
                emptyState.querySelector('p').textContent = 'Conversions trop rapides (< 1 jour) pour afficher la ventilation par secteur';
            } else {
                emptyState.classList.add('hidden');
            }
            if (velocityChart) {
                velocityChart.destroy();
                velocityChart = null;
            }
            return;
        }

        // Afficher le graphique
        chartWrapper.classList.remove('hidden');
        emptyState.classList.add('hidden');
        contentGrid.classList.add('md:grid-cols-2');

        // Trier par durée décroissante
        const sorted = labels.map((l, i) => ({ label: l, value: values[i] }))
            .sort((a, b) => b.value - a.value);

        const sortedLabels = sorted.map(s => s.label);
        const sortedValues = sorted.map(s => s.value);

        if (velocityChart) {
            velocityChart.destroy();
        }

        const ctx = canvas.getContext('2d');
        velocityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedLabels,
                datasets: [{
                    label: 'Jours moyens',
                    data: sortedValues,
                    backgroundColor: 'rgba(139, 92, 246, 0.7)',
                    borderColor: 'rgba(139, 92, 246, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(ctx) {
                                return ctx.raw > 0 ? ctx.raw + ' jours' : '< 1 jour';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: { display: true, text: 'Jours' }
                    }
                }
            }
        });

    } catch (error) {
        console.error('Erreur loadVelocity:', error);
    }
}

/**
 * Simulateur What-If - Initialisation et interaction
 */
function initWhatIfSimulator(data) {
    kpiData = data;

    const slider = document.getElementById('whatif-slider');
    const percentEl = document.getElementById('whatif-percent');
    const panierEl = document.getElementById('whatif-panier');
    const pipelineEl = document.getElementById('whatif-pipeline');
    const diffEl = document.getElementById('whatif-diff');

    if (!slider || !kpiData) return;

    function updateSimulation() {
        const variation = parseInt(slider.value) / 100;
        const percent = parseInt(slider.value);

        // Afficher pourcentage
        const sign = percent > 0 ? '+' : '';
        percentEl.textContent = sign + percent + '%';
        percentEl.className = 'font-bold ' + (percent > 0 ? 'text-green-600' : percent < 0 ? 'text-red-600' : 'text-blue-600');

        // Calculs
        const currentPanier = kpiData.panier_moyen || 0;
        const currentPipeline = kpiData.pipeline_pondere || 0;
        const newPanier = currentPanier * (1 + variation);
        const newPipeline = currentPipeline * (1 + variation);
        const diff = newPipeline - currentPipeline;

        // Affichage
        panierEl.textContent = formatMontant(newPanier);
        pipelineEl.textContent = formatMontant(newPipeline);

        // Différence avec couleur
        const diffSign = diff > 0 ? '+' : '';
        diffEl.textContent = diffSign + formatMontant(diff);
        diffEl.className = 'text-lg font-bold ' + (diff > 0 ? 'text-green-600' : diff < 0 ? 'text-red-600' : 'text-gray-800');
    }

    slider.addEventListener('input', updateSimulation);

    // Initialisation
    updateSimulation();
}

/**
 * Deals Froids - Chargement et affichage
 */
async function loadColdDeals(filters) {
    try {
        const data = await fetchColdDeals(filters);

        // Badge compteur dans le titre
        const badge = document.getElementById('cold-deals-badge');
        const nbCold = data.stats.nb_cold_deals;

        if (nbCold > 0) {
            badge.textContent = nbCold + ' deal' + (nbCold > 1 ? 's' : '');
            badge.className = 'ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ' +
                (nbCold > 5 ? 'bg-red-100 text-red-800' : 'bg-orange-100 text-orange-800');
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }

        // Badge dans les KPIs
        updateKpiBadge(nbCold);

        // Tableau ou message vide
        const emptyEl = document.getElementById('cold-deals-empty');
        const tableWrapper = document.getElementById('cold-deals-table-wrapper');
        const tbody = document.getElementById('table-cold-deals');

        if (nbCold === 0) {
            emptyEl.classList.remove('hidden');
            tableWrapper.classList.add('hidden');
            return;
        }

        emptyEl.classList.add('hidden');
        tableWrapper.classList.remove('hidden');

        tbody.innerHTML = data.cold_deals.map(d => {
            const badgeClass = d.jours_inactifs > 20
                ? 'bg-red-100 text-red-800'
                : 'bg-orange-100 text-orange-800';

            return `
                <tr class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="px-5 py-3 font-medium text-gray-800">${d.client || '-'}</td>
                    <td class="px-5 py-3">${getStatutBadge(d.statut)}</td>
                    <td class="px-5 py-3">${d.montant_formatted}</td>
                    <td class="px-5 py-3 text-gray-600">${d.secteur || '-'}</td>
                    <td class="px-5 py-3 text-gray-600">${d.assignee || '-'}</td>
                    <td class="px-5 py-3">
                        <span class="px-2 py-0.5 rounded-full text-xs font-medium ${badgeClass}">
                            ${d.jours_inactifs}j
                        </span>
                    </td>
                </tr>
            `;
        }).join('');

    } catch (error) {
        console.error('Erreur loadColdDeals:', error);
    }
}

/**
 * Met à jour le badge deals froids dans la section KPIs
 */
function updateKpiBadge(nbCold) {
    let badgeEl = document.getElementById('kpi-cold-badge');
    if (!badgeEl) return;

    if (nbCold > 0) {
        const colorClass = nbCold > 5 ? 'bg-red-100 text-red-700' : 'bg-orange-100 text-orange-700';
        badgeEl.innerHTML = `<span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${colorClass}">${nbCold} froid${nbCold > 1 ? 's' : ''}</span>`;
        badgeEl.classList.remove('hidden');
    } else {
        badgeEl.classList.add('hidden');
    }
}
