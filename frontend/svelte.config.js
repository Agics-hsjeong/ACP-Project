import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const lanOrigins = (process.env.LAN_TRUSTED_ORIGINS || '')
	.split(',')
	.map((s) => s.trim())
	.filter(Boolean);

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter(),
		csrf: {
			trustedOrigins: ['http://localhost:28433', 'http://127.0.0.1:28433', ...lanOrigins]
		}
	}
};

export default config;
