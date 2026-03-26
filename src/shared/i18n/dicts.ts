export const locales = {
  ru: {
    "upload-file": "Загрузите ваш файл",
    "allowed-file-types": "Разрешённые типы файлов",
  },
  en: {
    "upload-file": "Upload your file",
    "allowed-file-types": "Allowed file types",
  },
  fr: {
    "upload-file": "Téléchargez votre fichier",
    "allowed-file-types": "Types de fichiers autorisés",
  },
  de: {
    "upload-file": "Laden Sie Ihre Datei hoch",
    "allowed-file-types": "Zulässige Dateitypen",
  },
  zh: {
    "upload-file": "上传您的文件",
    "allowed-file-types": "允许的文件类型",
  },
} as const;

export type Locale = keyof typeof locales;
export type LocaleKey = keyof (typeof locales)["en"];
