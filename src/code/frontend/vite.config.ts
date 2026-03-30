import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src')
        }
    },
    css: {
        devSourcemap: true,
        modules: {
            generateScopedName: '[name]__[local]__[hash:base64:5]',
        }
    },
    build: {
        sourcemap: true
    },
    server: {
        port: 3000,
        open: true
    }
});
