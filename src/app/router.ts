import { t } from "@/shared/i18n";

const pages = import.meta.glob('@/pages/**/page.ts');

const root = document.getElementById('app');

function normalizePath (path: string) {
    return path.replace(/\/+$/, '') || '/';
}

export async function initRouter () {
    if (!root) return;

    const handleRoot = async () => {
        const path = normalizePath(window.location.pathname);
        const folder = path === '/' ? 'index' : path.slice(1);
        const pageKey = `/src/pages/${folder}/page.ts`;

        if (pages[pageKey]) {
            try {
                const mod = await pages[pageKey]() as { default: (el: HTMLElement) => void };
                root.innerHTML = '';
                mod.default(root);
            } catch (error) {
                console.error(`Error loading page: ${error}`);
                root.innerHTML = `<h1>${t('content-load-failed')}</h1>`;
            }
        } else {
            root.innerHTML = `<h1>404 ${t('page-not-found')}</h1>`;
        }
    };

    const onPopState = () => {
        handleRoot();
    };

    const onBodyClick = (e: MouseEvent) => {
        if (!(e.target instanceof Element)) return;
        const link = e.target.closest('a');
        if (
            link &&
            link.getAttribute('href')?.startsWith('/') &&
            !link.hasAttribute('download') &&
            link.getAttribute('target') !== '_blank' &&
            !e.ctrlKey &&
            !e.metaKey &&
            !e.shiftKey &&
            !e.altKey
        ) {
            e.preventDefault();
            const href = link.getAttribute('href');
            history.pushState({}, '', href);
            handleRoot();
        }
    };

    window.addEventListener('popstate', onPopState);
    window.addEventListener('click', onBodyClick);

    handleRoot();
}

export function navigate (path: string) {
    window.history.pushState({}, '', path);
    window.dispatchEvent(new PopStateEvent('popstate'));
}
