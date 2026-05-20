import Uppy from '@uppy/core';
import XHRUpload from '@uppy/xhr-upload';

import German from '@uppy/locales/lib/de_DE';
import French from '@uppy/locales/lib/fr_FR';
import Russian from '@uppy/locales/lib/ru_RU';
import Chinese from '@uppy/locales/lib/zh_CN';
import English from '@uppy/locales/lib/en_US';

import { currentLocale } from '@/shared/i18n';
import type { Locale } from '@uppy/utils';

const uppyLocales: Record<string, Locale> = {
  fr: French,
  de: German,
  ru: Russian,
  zh: Chinese,
  en: English
};

const allowedFileTypes = ['.dcm', '.nii', '.gz'];

export function createUploadUppy() {
  if (!uppyLocales[currentLocale]) {
    console.warn(`Uppy translations for '${currentLocale}' locale not found.`);
  }

  return new Uppy({
    locale: uppyLocales[currentLocale] ?? English,
    restrictions: {
      maxNumberOfFiles: 1,
      allowedFileTypes
    },
  }).use(XHRUpload, {
    endpoint: '/api/v1/upload/',
    fieldName: 'file',
    formData: true
  });
}

export { allowedFileTypes };
