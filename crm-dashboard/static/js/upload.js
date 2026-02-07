/**
 * Upload.js - Gestion de l'upload CSV avec drag & drop
 */

document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('csv-file-input');
    const fileName = document.getElementById('file-name');
    const btnUpload = document.getElementById('btn-upload');
    const spinner = document.getElementById('upload-spinner');
    const successMsg = document.getElementById('upload-success');
    const errorMsg = document.getElementById('upload-error');

    let selectedFile = null;
    const MAX_SIZE = 200 * 1024 * 1024; // 200MB

    function showFileName(file) {
        fileName.textContent = file.name;
        fileName.classList.remove('hidden');
        btnUpload.disabled = false;
    }

    function hideMessages() {
        successMsg.classList.add('hidden');
        errorMsg.classList.add('hidden');
    }

    function validateFile(file) {
        if (!file.name.toLowerCase().endsWith('.csv')) {
            errorMsg.textContent = 'Seuls les fichiers .csv sont acceptés';
            errorMsg.classList.remove('hidden');
            return false;
        }
        if (file.size > MAX_SIZE) {
            errorMsg.textContent = 'Le fichier dépasse la taille maximale de 200 MB';
            errorMsg.classList.remove('hidden');
            return false;
        }
        return true;
    }

    // Drag & Drop
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        hideMessages();
        const file = e.dataTransfer.files[0];
        if (file && validateFile(file)) {
            selectedFile = file;
            showFileName(file);
        }
    });

    // Sélection fichier via input
    fileInput.addEventListener('change', function() {
        hideMessages();
        const file = fileInput.files[0];
        if (file && validateFile(file)) {
            selectedFile = file;
            showFileName(file);
        }
    });

    // Upload
    btnUpload.addEventListener('click', async function() {
        if (!selectedFile) return;

        hideMessages();
        btnUpload.disabled = true;
        spinner.classList.remove('hidden');

        try {
            const result = await uploadCSV(selectedFile);
            successMsg.textContent = `Import réussi : ${result.nb_imported} deal(s) importé(s)`;
            if (result.nb_errors > 0) {
                successMsg.textContent += ` (${result.nb_errors} erreur(s) ignorée(s))`;
            }
            successMsg.classList.remove('hidden');

            // Reset
            selectedFile = null;
            fileName.classList.add('hidden');
            fileInput.value = '';

            // Rafraîchir le dashboard
            await refreshDashboard();
        } catch (error) {
            errorMsg.textContent = error.message || 'Erreur lors de l\'import';
            errorMsg.classList.remove('hidden');
            btnUpload.disabled = false;
        } finally {
            spinner.classList.add('hidden');
        }
    });
});
