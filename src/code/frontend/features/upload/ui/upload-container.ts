import styles from './upload-container.module.css';
import { t } from '@/shared/i18n';

export const uploadContainerHTML = `
  <div class="${styles.glassCard}">
      <h1 class="${styles.title}">${t("upload-file")}</h1>
      <div id="dashboard"></div>
  </div>`;
