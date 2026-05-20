import { defineConfig, loadEnv } from "vite";
import { heyApiPlugin } from "@hey-api/vite-plugin";
import path from "path";

export default defineConfig(({ mode }) => {
  process.env = { ...loadEnv(mode, process.cwd()), ...process.env };

  return {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    css: {
      devSourcemap: true,
      modules: {
        generateScopedName: "[name]__[local]__[hash:base64:5]",
      },
    },
    build: {
      sourcemap: true,
    },
    server: {
      port: 3000,
      open: true,
      middlewareMode: true,
    },
    plugins: [
      heyApiPlugin({
        config: {
          input: `${process.env.VITE_BACKEND_URL}/openapi.json`,
          output: "src/shared/api/generated",
        },
      }),
    ],
    appType: "spa",
  };
});
