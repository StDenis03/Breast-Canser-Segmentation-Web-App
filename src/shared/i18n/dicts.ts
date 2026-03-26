export const locales = {
  ru: {
    "upload-file": "Загрузите ваш файл",
    "allowed-file-types": "Разрешённые типы файлов",
    "content-load-failed": "Не удалось загрузить содержимое страницы",
    "page-not-found": "Страница не найдена"
  },
  en: {
    "upload-file": "Upload your file",
    "allowed-file-types": "Allowed file types",
    "content-load-failed": "Failed to load page content",
    "page-not-found": "Page not found"
  },
  fr: {
    "upload-file": "Téléchargez votre fichier",
    "allowed-file-types": "Types de fichiers autorisés",
    "content-load-failed": "Échec du chargement du contenu de la page",
    "page-not-found": "Page non trouvée"
  },
  de: {
    "upload-file": "Laden Sie Ihre Datei hoch",
    "allowed-file-types": "Zulässige Dateitypen",
    "content-load-failed": "Seiteninhalt konnte nicht geladen werden",
    "page-not-found": "Seite nicht gefunden"
  },
  zh: {
    "upload-file": "上传您的文件",
    "allowed-file-types": "允许的文件类型",
    "content-load-failed": "页面内容加载失败",
    "page-not-found": "页面未找到"
  },
} as const;

export type Locale = keyof typeof locales;
export type LocaleKey = keyof (typeof locales)["en"];
