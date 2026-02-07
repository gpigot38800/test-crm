/**
 * Performance.js - Graphique et tableau de performance commerciale
 */

let performanceChart = null;

async function initPerformanceChart(filters) {
    try {
        const data = await fetchPerformance(filters);
        const canvas = document.getElementById('chart-performance');
        const emptyMsg = document.getElementById('performance-chart-empty');

        if (!data.performance || data.performance.length === 0) {
            canvas.style.display = 'none';
            emptyMsg.classList.remove('hidden');
            renderPerformanceTable([]);
            return;
        }

        canvas.style.display = 'block';
        emptyMsg.classList.add('hidden');

        // Détruire le chart existant
        if (performanceChart) {
            performanceChart.destroy();
        }

        const ctx = canvas.getContext('2d');
        performanceChart = new Chart(ctx, {
            type: 'bar',
            data: data.chart_data,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Nombre de Deals'
                        },
                        beginAtZero: true
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Taux de Conversion (%)'
                        },
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(ctx) {
                                if (ctx.dataset.yAxisID === 'y1') {
                                    return ctx.dataset.label + ': ' + ctx.parsed.y + '%';
                                }
                                return ctx.dataset.label + ': ' + ctx.parsed.y;
                            }
                        }
                    }
                }
            }
        });

        renderPerformanceTable(data.performance);

    } catch (error) {
        console.error('Erreur initPerformanceChart:', error);
    }
}

function renderPerformanceTable(performance) {
    const tbody = document.getElementById('table-performance');

    if (!performance || performance.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="px-4 py-4 text-gray-400 text-center">Aucune donnée</td></tr>';
        return;
    }

    tbody.innerHTML = performance.map(p => `
        <tr class="border-b border-gray-100 hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-800">${p.assignee}</td>
            <td class="px-4 py-3">${p.nb_deals}</td>
            <td class="px-4 py-3">${p.montant_total_formatted}</td>
            <td class="px-4 py-3">${p.pipeline_pondere_formatted}</td>
            <td class="px-4 py-3">${p.panier_moyen_formatted}</td>
            <td class="px-4 py-3 font-medium">${p.taux_conversion}%</td>
        </tr>
    `).join('');
}
