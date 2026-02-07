/**
 * Filters.js - Gestion de la sidebar de filtres avec persistance localStorage
 */

(function() {
    const STORAGE_KEY = 'crm_filters';

    async function loadFilterOptions() {
        try {
            const options = await fetchFilterOptions();
            renderCheckboxes('filter-statuts', options.statuts, 'statut');
            renderCheckboxes('filter-secteurs', options.secteurs, 'secteur');
            renderCheckboxes('filter-assignees', options.assignees, 'assignee');

            // Restaurer les filtres sauvegardés
            restoreFilters();
        } catch (error) {
            console.error('Erreur loadFilterOptions:', error);
        }
    }

    function renderCheckboxes(containerId, values, name) {
        const container = document.getElementById(containerId);
        if (!values || values.length === 0) {
            container.innerHTML = '<p class="text-xs text-gray-400">Aucune option</p>';
            return;
        }
        container.innerHTML = values.map(value => `
            <label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                <input type="checkbox" name="${name}" value="${value}" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <span>${value}</span>
            </label>
        `).join('');
    }

    function getActiveFilters() {
        const filters = {};

        // Statuts cochés
        const statuts = Array.from(document.querySelectorAll('input[name="statut"]:checked')).map(cb => cb.value);
        if (statuts.length) filters.statut = statuts;

        // Secteurs cochés
        const secteurs = Array.from(document.querySelectorAll('input[name="secteur"]:checked')).map(cb => cb.value);
        if (secteurs.length) filters.secteur = secteurs;

        // Assignees cochés
        const assignees = Array.from(document.querySelectorAll('input[name="assignee"]:checked')).map(cb => cb.value);
        if (assignees.length) filters.assignee = assignees;

        // Dates
        const dateFrom = document.getElementById('filter-date-from').value;
        if (dateFrom) filters.date_from = dateFrom;

        const dateTo = document.getElementById('filter-date-to').value;
        if (dateTo) filters.date_to = dateTo;

        // Recherche
        const search = document.getElementById('filter-search').value.trim();
        if (search) filters.search = search;

        return Object.keys(filters).length > 0 ? filters : null;
    }

    function saveFilters(filters) {
        if (filters) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
        } else {
            localStorage.removeItem(STORAGE_KEY);
        }
    }

    function restoreFilters() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) return;

        try {
            const filters = JSON.parse(saved);

            // Restaurer checkboxes
            if (filters.statut) {
                filters.statut.forEach(s => {
                    const cb = document.querySelector(`input[name="statut"][value="${s}"]`);
                    if (cb) cb.checked = true;
                });
            }
            if (filters.secteur) {
                filters.secteur.forEach(s => {
                    const cb = document.querySelector(`input[name="secteur"][value="${s}"]`);
                    if (cb) cb.checked = true;
                });
            }
            if (filters.assignee) {
                filters.assignee.forEach(a => {
                    const cb = document.querySelector(`input[name="assignee"][value="${a}"]`);
                    if (cb) cb.checked = true;
                });
            }

            // Restaurer dates
            if (filters.date_from) document.getElementById('filter-date-from').value = filters.date_from;
            if (filters.date_to) document.getElementById('filter-date-to').value = filters.date_to;

            // Restaurer recherche
            if (filters.search) document.getElementById('filter-search').value = filters.search;
        } catch (e) {
            console.error('Erreur restauration filtres:', e);
        }
    }

    function applyFilters() {
        const filters = getActiveFilters();
        saveFilters(filters);
        refreshDashboard(filters);

        // Fermer la sidebar sur mobile
        const sidebar = document.getElementById('sidebar');
        const backdrop = document.getElementById('sidebar-backdrop');
        if (window.innerWidth < 1024) {
            sidebar.classList.add('-translate-x-full');
            backdrop.classList.add('hidden');
        }
    }

    function resetFilters() {
        // Décocher toutes les checkboxes
        document.querySelectorAll('#sidebar input[type="checkbox"]').forEach(cb => cb.checked = false);

        // Vider les champs date
        document.getElementById('filter-date-from').value = '';
        document.getElementById('filter-date-to').value = '';

        // Vider la recherche
        document.getElementById('filter-search').value = '';

        // Supprimer du localStorage
        localStorage.removeItem(STORAGE_KEY);

        // Rafraîchir sans filtres
        refreshDashboard(null);
    }

    // Event listeners
    const btnApply = document.getElementById('btn-apply-filters');
    const btnReset = document.getElementById('btn-reset-filters');

    if (btnApply) btnApply.addEventListener('click', applyFilters);
    if (btnReset) btnReset.addEventListener('click', resetFilters);

    // Charger les options au démarrage
    document.addEventListener('DOMContentLoaded', loadFilterOptions);
})();
