/**
 * Charts.js - Configuration et rendu des graphiques Chart.js
 */

let chartMontants = null;
let chartPanierMoyen = null;

function formatEuro(value) {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(value);
}

async function initSectorCharts(filters) {
    try {
        const data = await fetchSectorAnalytics(filters);

        // Graphique Montants Totaux par Secteur
        const ctxMontants = document.getElementById('chart-montants-secteurs');
        if (ctxMontants && data.chart_montants.labels.length > 0) {
            if (chartMontants) chartMontants.destroy();
            chartMontants = new Chart(ctxMontants, {
                type: 'bar',
                data: data.chart_montants,
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: { duration: 800 },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(ctx) { return formatEuro(ctx.parsed.x); }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                callback: function(value) { return formatEuro(value); }
                            }
                        },
                        y: {
                            ticks: { autoSkip: false }
                        }
                    }
                }
            });
            // Ajuster hauteur du canvas selon le nombre de secteurs
            const nbLabels = data.chart_montants.labels.length;
            ctxMontants.parentElement.style.height = Math.max(300, nbLabels * 28) + 'px';
        }

        // Graphique Top 5 Paniers Moyens
        const ctxPanier = document.getElementById('chart-panier-moyen');
        if (ctxPanier && data.chart_panier_moyen.labels.length > 0) {
            if (chartPanierMoyen) chartPanierMoyen.destroy();
            chartPanierMoyen = new Chart(ctxPanier, {
                type: 'bar',
                data: data.chart_panier_moyen,
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: { duration: 800 },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(ctx) { return formatEuro(ctx.parsed.x); }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                callback: function(value) { return formatEuro(value); }
                            }
                        },
                        y: {
                            ticks: { autoSkip: false }
                        }
                    }
                }
            });
            ctxPanier.parentElement.style.height = '200px';
        }

        // Tableau récapitulatif
        renderSectorTable(data.tableau);

    } catch (error) {
        console.error('Erreur initSectorCharts:', error);
    }
}

function renderSectorTable(tableau) {
    const tbody = document.getElementById('table-secteurs');
    if (!tbody) return;

    if (!tableau || tableau.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="px-5 py-4 text-gray-400 text-center">Aucune donnée</td></tr>';
        return;
    }

    // Déjà trié par montant total décroissant côté serveur
    const rows = tableau.map(row => `
        <tr class="border-b border-gray-100 hover:bg-gray-50">
            <td class="px-5 py-3 font-medium text-gray-800">${row.secteur}</td>
            <td class="px-5 py-3">${row.montant_total_formatted}</td>
            <td class="px-5 py-3">${row.panier_moyen_formatted}</td>
            <td class="px-5 py-3">${row.nb_deals}</td>
            <td class="px-5 py-3">${row.valeur_ponderee_formatted}</td>
        </tr>
    `).join('');

    tbody.innerHTML = rows;
}
