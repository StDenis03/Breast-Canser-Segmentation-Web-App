import { createUploadUppy, allowedFileTypes } from '@/features/upload/model/create-uppy';
import { uploadContainerHTML } from '@/features/upload/ui/upload-container';

import Dashboard from '@uppy/dashboard';

import styles from './page.module.css';

import { t } from '@/shared/i18n';

import '@uppy/core/css/style.min.css';
import '@uppy/dashboard/css/style.min.css';

let currentStudyId: number | null = null;
let pollInterval: number | null = null;
let phraseInterval: number | null = null;

const PROCESSING_PHRASE_KEYS = [
  'phrase-loading',
  'phrase-analyzing',
  'phrase-detecting',
  'phrase-segmenting',
  'phrase-model',
  'phrase-volume',
  'phrase-mask',
  'phrase-almost',
] as const;

async function checkStatus(studyId: number): Promise<any> {
  try {
    const response = await fetch(`/api/v1/result/${studyId}/status`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error checking status:', error);
    throw error;
  }
}

async function downloadResult(studyId: number): Promise<void> {
  try {
    const response = await fetch(`/api/v1/result/${studyId}`);
    if (!response.ok) {
      throw new Error('Failed to download result');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `segmentation_${studyId}.nii.gz`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error('Error downloading result:', error);
    alert(t('failed'));
  }
}

function stopPhrases() {
  if (phraseInterval) {
    clearInterval(phraseInterval);
    phraseInterval = null;
  }
}

function startPhrases() {
  stopPhrases();
  let idx = 0;

  const setPhrase = (text: string) => {
    const el = document.getElementById('statusText');
    if (!el) return;
    el.classList.add(styles.phraseExit);
    setTimeout(() => {
      if (!phraseInterval) return; // stopped before timeout fired
      const el2 = document.getElementById('statusText');
      if (!el2) return;
      el2.textContent = text;
      el2.classList.remove(styles.phraseExit);
      el2.classList.add(styles.phraseEnter);
      setTimeout(() => el2.classList.remove(styles.phraseEnter), 400);
    }, 250);
  };

  // Set first phrase immediately without animation
  const el = document.getElementById('statusText');
  if (el) el.textContent = t(PROCESSING_PHRASE_KEYS[0]);

  phraseInterval = window.setInterval(() => {
    idx = (idx + 1) % PROCESSING_PHRASE_KEYS.length;
    const el = document.getElementById('statusText');
    if (!el) { stopPhrases(); return; }
    setPhrase(t(PROCESSING_PHRASE_KEYS[idx]));
  }, 3000);
}

function showUploadForm() {
  const container = document.getElementById('app');
  if (!container) return;

  container.innerHTML = `
    <section class="${styles.uploadWrapper}">
      ${uploadContainerHTML}
    </section>
  `;

  const uppy = createUploadUppy();

  uppy.use(Dashboard, {
    target: '#dashboard',
    inline: true,
    height: 350,
    proudlyDisplayPoweredByUppy: false,
    note: `${t('allowed-file-types')}: ${allowedFileTypes.join(', ')}`,
    theme: 'auto'
  });

  uppy.on('upload-success', (_file: any, response: any) => {
    const responseData = response.body as any;
    currentStudyId = responseData.study_id;
    showResultStatus();
    startPolling();
  });

  uppy.on('upload-error', (_file: any, error: any) => {
    console.error('Upload error:', error);
    alert('Upload failed: ' + error.message);
  });
}

function showResultStatus() {
  if (!currentStudyId) {
    showUploadForm();
    return;
  }

  const container = document.getElementById('app');
  if (!container) return;

  container.innerHTML = `
    <section class="${styles.uploadWrapper}">
      <div class="${styles.glassCard}">
        <h1 class="${styles.title}">${t('result')}</h1>
        <div class="${styles.statusContainer}">
          <div class="${styles.ring}" id="statusIcon">
          </div>
          <div class="${styles.statusText}" id="statusText">${t(PROCESSING_PHRASE_KEYS[0])}</div>
          <div class="${styles.statusSub}" id="statusSub">${t('est-time')}</div>
        </div>
        <div class="${styles.actions}">
          <button id="downloadBtn" class="${styles.button} ${styles.primaryButton} ${styles.buttonDisabled}" disabled onclick="downloadResult(${currentStudyId})">
             ${t('download-result')}
             
          </button>
          <button id="uploadBtn" class="${styles.button} ${styles.secondaryButton} ${styles.buttonDisabled}" disabled onclick="location.reload()">
            ${t('upload-another')}
          </button>
        </div>
      </div>
    </section>
  `;

  // Make downloadResult available globally
  (window as any).downloadResult = downloadResult;
}

function startPolling() {
  if (!currentStudyId) return;

  if (pollInterval) clearInterval(pollInterval);

  startPhrases();

  let pollCount = 0;
  const maxPolls = 600; // 10 minutes

  const updateStatus = async () => {
    if (pollCount >= maxPolls) {
      if (pollInterval) clearInterval(pollInterval);
      stopPhrases();
      return;
    }

    try {
      const status = await checkStatus(currentStudyId!);
      const downloadBtn = document.getElementById('downloadBtn');
      const uploadBtn = document.getElementById('uploadBtn');

      const iconEl  = document.getElementById('statusIcon');
      const textEl  = document.getElementById('statusText');
      const subEl   = document.getElementById('statusSub');

      if (status.status === 'completed') {
        stopPhrases();

        if (iconEl) {
          iconEl.className = `${styles.statusIcon} ${styles.statusIconCompleted}`;
          iconEl.textContent = '✓';
        }
        if (textEl) textEl.innerHTML = t('completed');
        if (subEl)  subEl.textContent = '';

        if (downloadBtn && downloadBtn instanceof HTMLButtonElement) {
          downloadBtn.disabled = false;
          downloadBtn.classList.remove(styles.buttonDisabled);
        }

        if (uploadBtn && uploadBtn instanceof HTMLButtonElement) {
          uploadBtn.disabled = false;
          uploadBtn.classList.remove(styles.buttonDisabled);
        }
        
        if (pollInterval) clearInterval(pollInterval);
      } else if (status.status === 'failed') {
        stopPhrases();

        if (iconEl) {
          iconEl.className = `${styles.statusIcon} ${styles.statusIconFailed}`;
          iconEl.textContent = '✕';
        }
        if (textEl) textEl.innerHTML = t('failed');
        if (subEl)  subEl.textContent = '';

        if (downloadBtn) downloadBtn.style.display = 'none';

        if (pollInterval) clearInterval(pollInterval);
      }
    } catch (error) {
      console.error('Error checking status:', error);
    }

    pollCount++;
  };

  pollInterval = window.setInterval(updateStatus, 1000);
  updateStatus(); // Check immediately
}

export default function render(_container: HTMLElement) {
  showUploadForm();
}
