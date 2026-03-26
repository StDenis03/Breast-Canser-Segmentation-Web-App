import Uppy from '@uppy/core';
import Dashboard from '@uppy/dashboard';
import styles from './style.module.css';

import '@uppy/core/css/style.min.css';
import '@uppy/dashboard/css/style.min.css';

export default function render(container: HTMLElement) {
    container.innerHTML = `
      <section class="${styles.uploadWrapper}">
          <div class="${styles.glassCard}">
              <h1 class="${styles.title}">Upload your file</h1>
              <div id="dashboard"></div>
          </div>
      </section>
    `;

    new Uppy({
      restrictions: { maxNumberOfFiles: 1 }
    })
    .use(Dashboard, {
      target: '#dashboard',
      inline: true,
      height: 350,
      proudlyDisplayPoweredByUppy: false
    });
}
