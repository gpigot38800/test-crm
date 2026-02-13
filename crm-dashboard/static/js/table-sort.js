/**
 * Gestion du tri du tableau des deals
 */

// État du tri
let currentSort = {
    column: null,
    direction: 'asc' // 'asc' ou 'desc'
};

// Stockage des deals pour le tri
let allDealsData = [];

/**
 * Initialise le tri du tableau
 */
function initTableSort() {
    // Sélectionner tous les en-têtes avec data-sort
    const headers = document.querySelectorAll('th[data-sort]');

    headers.forEach(header => {
        header.addEventListener('click', function() {
            const column = this.dataset.sort;
            sortTable(column);
        });
    });
}

/**
 * Trie le tableau selon la colonne spécifiée
 * @param {string} column - Nom de la colonne à trier
 */
function sortTable(column) {
    // Si on clique sur la même colonne, inverser la direction
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        // Nouvelle colonne : tri croissant par défaut
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    // Trier les données
    const sortedDeals = sortDeals(allDealsData, column, currentSort.direction);

    // Mettre à jour l'affichage
    updateTableDisplay(sortedDeals);

    // Mettre à jour les icônes de tri
    updateSortIcons(column, currentSort.direction);
}

/**
 * Trie un tableau de deals
 * @param {Array} deals - Tableau des deals
 * @param {string} column - Colonne de tri
 * @param {string} direction - Direction ('asc' ou 'desc')
 * @returns {Array} Tableau trié
 */
function sortDeals(deals, column, direction) {
    const sortedArray = [...deals]; // Copie pour ne pas modifier l'original

    sortedArray.sort((a, b) => {
        let valA, valB;

        switch(column) {
            case 'client':
                valA = (a.client || '').toLowerCase();
                valB = (b.client || '').toLowerCase();
                return direction === 'asc'
                    ? valA.localeCompare(valB)
                    : valB.localeCompare(valA);

            case 'statut':
                // Ordre logique des statuts
                const statutOrder = { 'Prospect': 1, 'Qualifié': 2, 'Négociation': 3, 'Gagné': 4 };
                valA = statutOrder[a.statut] || 0;
                valB = statutOrder[b.statut] || 0;
                return direction === 'asc' ? valA - valB : valB - valA;

            case 'montant':
                valA = parseFloat(a.montant_brut) || 0;
                valB = parseFloat(b.montant_brut) || 0;
                return direction === 'asc' ? valA - valB : valB - valA;

            case 'secteur':
                valA = (a.secteur || '').toLowerCase();
                valB = (b.secteur || '').toLowerCase();
                return direction === 'asc'
                    ? valA.localeCompare(valB)
                    : valB.localeCompare(valA);

            case 'commercial':
                valA = (a.assignee || '').toLowerCase();
                valB = (b.assignee || '').toLowerCase();
                return direction === 'asc'
                    ? valA.localeCompare(valB)
                    : valB.localeCompare(valA);

            case 'echeance':
                // Dates nulles en dernier
                if (!a.date_echeance && !b.date_echeance) return 0;
                if (!a.date_echeance) return 1;
                if (!b.date_echeance) return -1;

                valA = new Date(a.date_echeance).getTime();
                valB = new Date(b.date_echeance).getTime();
                return direction === 'asc' ? valA - valB : valB - valA;

            default:
                return 0;
        }
    });

    return sortedArray;
}

/**
 * Met à jour l'affichage du tableau avec les données triées
 * @param {Array} deals - Tableau des deals triés
 */
function updateTableDisplay(deals) {
    const tbody = document.getElementById('table-deals');

    if (!deals || deals.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="px-4 py-4 text-gray-400 text-center">Aucun deal trouvé</td></tr>';
        return;
    }

    // Régénérer les lignes du tableau
    tbody.innerHTML = deals.map(deal => {
        const statutClass = getStatutClass(deal.statut);
        const montantFormatted = formatMontant(deal.montant_brut);
        const dateFormatted = deal.date_echeance
            ? new Date(deal.date_echeance).toLocaleDateString('fr-FR')
            : '-';

        const dealJson = JSON.stringify(deal).replace(/'/g, "&#39;");
        const clientEscaped = (deal.client || '').replace(/"/g, '&quot;');

        return `
            <tr class="border-b border-gray-100 hover:bg-gray-50">
                <td class="px-4 py-3 font-medium text-gray-800">${escapeHtml(deal.client || '-')}</td>
                <td class="px-4 py-3">
                    <span class="statut-badge px-2 py-0.5 rounded-full text-xs font-medium ${statutClass}">
                        ${escapeHtml(deal.statut)}
                    </span>
                </td>
                <td class="px-4 py-3">${montantFormatted}</td>
                <td class="px-4 py-3 text-gray-600">${escapeHtml(deal.secteur || '-')}</td>
                <td class="px-4 py-3 text-gray-600">${escapeHtml(deal.assignee || '-')}</td>
                <td class="px-4 py-3">${dateFormatted}</td>
                <td class="px-4 py-3">
                    <div class="flex gap-2">
                        <button class="btn-edit text-blue-600 hover:text-blue-800 text-xs font-medium" data-deal='${dealJson}'>Modifier</button>
                        <button class="btn-delete text-red-600 hover:text-red-800 text-xs font-medium" data-id="${deal.id}" data-client="${clientEscaped}" data-montant="${deal.montant_brut}">Supprimer</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');

    // Ré-attacher les événements sur les boutons "Modifier"
    attachEditDealEvents();
}

/**
 * Met à jour les icônes de tri dans les en-têtes
 * @param {string} activeColumn - Colonne active
 * @param {string} direction - Direction du tri
 */
function updateSortIcons(activeColumn, direction) {
    // Réinitialiser toutes les icônes
    document.querySelectorAll('th[data-sort] .sort-icon').forEach(icon => {
        icon.textContent = '⇅';
        icon.classList.remove('opacity-100');
        icon.classList.add('opacity-30');
    });

    // Mettre à jour l'icône de la colonne active
    const activeHeader = document.querySelector(`th[data-sort="${activeColumn}"] .sort-icon`);
    if (activeHeader) {
        activeHeader.textContent = direction === 'asc' ? '↑' : '↓';
        activeHeader.classList.remove('opacity-30');
        activeHeader.classList.add('opacity-100');
    }
}

/**
 * Sauvegarde les données des deals pour le tri
 * @param {Array} deals - Tableau des deals
 */
function saveDealsForSorting(deals) {
    allDealsData = deals || [];
}

/**
 * Retourne la classe CSS pour un statut
 * @param {string} statut - Statut du deal
 * @returns {string} Classes CSS
 */
function getStatutClass(statut) {
    const classes = {
        'Prospect': 'bg-gray-100 text-gray-800',
        'Qualifié': 'bg-blue-100 text-blue-800',
        'Négociation': 'bg-yellow-100 text-yellow-800',
        'Gagné': 'bg-green-100 text-green-800'
    };
    return classes[statut] || 'bg-gray-100 text-gray-800';
}

/**
 * Formate un montant en euros
 * @param {number} montant - Montant à formater
 * @returns {string} Montant formaté
 */
function formatMontant(montant) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(montant);
}

/**
 * Échappe les caractères HTML pour éviter les injections XSS
 * @param {string} text - Texte à échapper
 * @returns {string} Texte échappé
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Ré-attache les événements sur les boutons "Modifier" et "Supprimer"
 */
function attachEditDealEvents() {
    const tbody = document.getElementById('table-deals');

    // Boutons "Modifier"
    tbody.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', function() {
            const deal = JSON.parse(this.dataset.deal);
            if (window.openDealModal) {
                window.openDealModal('edit', deal);
            }
        });
    });

    // Boutons "Supprimer"
    tbody.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const client = this.dataset.client;
            const montant = this.dataset.montant;
            if (window.handleDeleteDeal) {
                window.handleDeleteDeal(id, client, montant);
            }
        });
    });
}

// Initialiser au chargement du DOM
document.addEventListener('DOMContentLoaded', initTableSort);
