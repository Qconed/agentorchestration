const cvDropZone = document.getElementById('drop-cv');
const offerDropZone = document.getElementById('drop-offer');
const inputCv = document.getElementById('input-cv');
const inputOffer = document.getElementById('input-offer');
const cvInfo = document.getElementById('cv-info');
const offerInfo = document.getElementById('offer-info');
const btnGenerate = document.getElementById('btn-generate');
const btnModify = document.getElementById('btn-modify');
const btnDownload = document.getElementById('btn-download');
const previewSection = document.getElementById('preview-section');
const letterPreview = document.getElementById('letter-preview');
const modifyPrompt = document.getElementById('modify-prompt');
const loader = document.getElementById('loader');

let files = { cv: null, offer: null };

// --- Event Listeners ---

// Drop Zone Events
[cvDropZone, offerDropZone].forEach(zone => {
    zone.addEventListener('click', () => {
        const input = zone.id === 'drop-cv' ? inputCv : inputOffer;
        input.click();
    });

    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('dragover');
    });

    zone.addEventListener('dragleave', () => {
        zone.classList.remove('dragover');
    });

    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        handleFileSelect(file, zone.id === 'drop-cv' ? 'cv' : 'offer');
    });
});

inputCv.addEventListener('change', (e) => handleFileSelect(e.target.files[0], 'cv'));
inputOffer.addEventListener('change', (e) => handleFileSelect(e.target.files[0], 'offer'));

function handleFileSelect(file, type) {
    if (file && file.type === 'application/pdf') {
        files[type] = file;
        const info = type === 'cv' ? cvInfo : offerInfo;
        const zone = type === 'cv' ? cvDropZone : offerDropZone;
        
        info.textContent = file.name;
        zone.classList.add('active');
        
        checkReady();
    } else {
        alert("Veuillez sélectionner un fichier PDF valide.");
    }
}

function checkReady() {
    btnGenerate.disabled = !(files.cv && files.offer);
}

// Actions
btnGenerate.addEventListener('click', async () => {
    showLoader();
    try {
        // 1. Upload
        const formData = new FormData();
        formData.append('cv', files.cv);
        formData.append('offer', files.offer);

        const uploadRes = await fetch('/upload', { method: 'POST', body: formData });
        const uploadData = await uploadRes.json();
        if (uploadData.error) throw new Error(uploadData.error);

        // 2. Generate
        const genRes = await fetch('/generate', { method: 'POST' });
        const genData = await genRes.json();
        if (genData.error) throw new Error(genData.error);

        displayLetter(genData.letter);
    } catch (err) {
        alert("Erreur: " + err.message);
    } finally {
        hideLoader();
    }
});

btnModify.addEventListener('click', async () => {
    const prompt = modifyPrompt.value.trim();
    if (!prompt) return;

    showLoader();
    try {
        const formData = new FormData();
        formData.append('prompt', prompt);

        const modRes = await fetch('/modify', { method: 'POST', body: formData });
        const modData = await modRes.json();
        if (modData.error) throw new Error(modData.error);

        displayLetter(modData.letter);
        modifyPrompt.value = "";
    } catch (err) {
        alert("Erreur: " + err.message);
    } finally {
        hideLoader();
    }
});

btnDownload.addEventListener('click', () => {
    window.location.href = '/download';
});

// --- Helpers ---

function displayLetter(text) {
    letterPreview.innerText = text;
    previewSection.classList.remove('hidden');
    previewSection.scrollIntoView({ behavior: 'smooth' });
}

function showLoader() { loader.classList.remove('hidden'); }
function hideLoader() { loader.classList.add('hidden'); }
