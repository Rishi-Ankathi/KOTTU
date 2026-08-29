import { defineConfig } from "astro/config";

// KOTTU marketing + tool site.
// Fully static output - `npm run build` emits ./dist which opens on any
// static host (or straight from the filesystem). No server, no backend.
export default defineConfig({
  build: { format: "directory" },
  devToolbar: { enabled: false },
});
