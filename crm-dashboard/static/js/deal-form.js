/**
 * Deal Form - Gestion du modal de création/édition de deals
 */

(function() {
    const modal = document.getElementById('deal-modal');
    const form = document.getElementById('deal-form');
    const titleEl = document.getElementById('modal-title');
    const errorEl = document.getElementById('deal-form-error');
    const btnNew = document.getElementById('btn-new-deal');
    const btnClose = document.getElementById('btn-modal-close');
    const btnCancel = document.getElementById('btn-modal-cancel');
    const btnSave = document.getElementById('btn-modal-save');

    let editingDealId = null;

    function openDealModal(mode, dealData) {
        editingDealId = null;
        form.reset();
        errorEl.classList.add('hidden');

        if (mode === 'edit' && dealData) {
            editingDealId = dealData.id;
            titleEl.textContent = 'Modifier le Deal';
            document.getElementById('deal-id').value = dealData.id;
            document.getElementById('deal-client').value = dealData.client || '';
            document.getElementById('deal-statut').value = dealData.statut || '';
            document.getElementById('deal-montant').value = dealData.montant_brut || '';
            document.getElementById('deal-secteur').value = dealData.secteur || '';
            document.getElementById('deal-echeance').value = dealData.date_echeance || '';
            document.getElementById('deal-assignee').value = dealData.assignee || '';
            document.getElementById('deal-notes').value = dealData.notes || '';
        } else {
            titleEl.textContent = 'Nouveau Deal';
        }

        modal.classList.remove('hidden');
    }

    function closeDealModal() {
        modal.classList.add('hidden');
        editingDealId = null;
    }

    async function handleSubmit() {
        // Validation HTML5
        if (!form.reportValidity()) return;

        const montant = parseFloat(document.getElementById('deal-montant').value);
        if (isNaN(montant) || montant <= 0) {
            errorEl.textContent = 'Le montant doit être supérieur à 0';
            errorEl.classList.remove('hidden');
            return;
        }

        const data = {
            client: document.getElementById('deal-client').value.trim(),
            statut: document.getElementById('deal-statut').value,
            montant_brut: montant,
            secteur: document.getElementById('deal-secteur').value.trim() || null,
            date_echeance: document.getElementById('deal-echeance').value || null,
            assignee: document.getElementById('deal-assignee').value.trim() || null,
            notes: document.getElementById('deal-notes').value.trim() || null
        };

        try {
            btnSave.disabled = true;
            btnSave.textContent = 'Enregistrement...';

            if (editingDealId) {
                await updateDeal(editingDealId, data);
            } else {
                await createDeal(data);
            }

            closeDealModal();
            refreshDashboard(currentFilters);
        } catch (error) {
            errorEl.textContent = error.message || 'Erreur lors de la sauvegarde';
            errorEl.classList.remove('hidden');
        } finally {
            btnSave.disabled = false;
            btnSave.textContent = 'Enregistrer';
        }
    }

    // Expose globalement pour main.js
    window.openDealModal = openDealModal;

    // Suppression avec confirmation
    window.handleDeleteDeal = async function(id, client, montant) {
        const formattedMontant = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 }).format(montant) + ' \u20AC';
        if (!confirm(`Supprimer le deal "${client}" (${formattedMontant}) ?`)) return;

        try {
            await deleteDeal(id);
            refreshDashboard(currentFilters);
        } catch (error) {
            alert('Erreur lors de la suppression : ' + error.message);
        }
    };

    // Event listeners
    if (btnNew) btnNew.addEventListener('click', () => openDealModal('create'));
    if (btnClose) btnClose.addEventListener('click', closeDealModal);
    if (btnCancel) btnCancel.addEventListener('click', closeDealModal);
    if (btnSave) btnSave.addEventListener('click', handleSubmit);

    // Fermeture par clic sur le backdrop
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeDealModal();
        });
    }

    // Fermeture par touche Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeDealModal();
        }
    });
})();
