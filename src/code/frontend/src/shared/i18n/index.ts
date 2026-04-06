import { locales, type Locale, type LocaleKey } from "./dicts";

const DEFAULT_LOCALE = 'en';
export const currentLocale: Locale = navigator.language.split('-')[0] as Locale || DEFAULT_LOCALE;

/** 
 * Gets translation with params 
 * @example
 * button.textContent = t('example-translation', { param: 'Example' });
 */
export function t (key: LocaleKey, params?: Record<string, string>) {
    const text = locales[currentLocale][key] || (key as string);

    if (params) {
        Object.entries(params).forEach(([k, v]) => {
            text.replace(`{{${k}}`, v);
        })
    }

    return text;
}
