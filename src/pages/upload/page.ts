import Uppy from '@uppy/core';

import German from '@uppy/locales/lib/de_DE';
import French from '@uppy/locales/lib/fr_FR';
import Russian from '@uppy/locales/lib/ru_RU';
import Chinese from '@uppy/locales/lib/zh_CN';

import { currentLocale } from '@/shared/i18n';
import { t } from '@/shared/i18n';

import Dashboard from '@uppy/dashboard';
import styles from './style.module.css';

import '@uppy/core/css/style.min.css';
import '@uppy/dashboard/css/style.min.css';

// English by default, not listed
const uppyLocales: Record<string, any> = {
  'fr': French,
  'de': German,
  'ru': Russian,
  'zh': Chinese
};

const allowedFileTypes = ['dcm', 'dic', 'dicom'];

if (!uppyLocales[currentLocale]) {
  console.warn(`Uppy translations for '${currentLocale}' locale not found.`);
}

export default function render(container: HTMLElement) {
    container.innerHTML = `
      <section class="${styles.uploadWrapper}">
          <div class="${styles.glassCard}">
              <h1 class="${styles.title}">${t('upload-file')}</h1>
              <div id="dashboard"></div>
          </div>
      </section>
    `;

    new Uppy({
      locale: uppyLocales[currentLocale],
      restrictions: { maxNumberOfFiles: 1, allowedFileTypes: allowedFileTypes }
    })
    .use(Dashboard, {
      target: '#dashboard',
      inline: true,
      height: 350,
      proudlyDisplayPoweredByUppy: false,
      note: `${t('allowed-file-types')}: ${allowedFileTypes.join(', ')}`
    });
}
