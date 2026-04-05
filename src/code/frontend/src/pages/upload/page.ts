import { createUploadUppy, allowedFileTypes } from '@/features/upload/model/create-uppy';
import { uploadContainerHTML } from '@/features/upload/ui/upload-container';

import Dashboard from '@uppy/dashboard';

import styles from './page.module.css';

import { t } from '@/shared/i18n';

import '@uppy/core/css/style.min.css';
import '@uppy/dashboard/css/style.min.css';

export default function render(container: HTMLElement) {
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
    theme: 'dark'
  });
}
