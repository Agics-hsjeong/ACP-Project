import { apiHealth } from '$lib/api/client';
import { fetchLandingContent, type LandingFeature } from '$lib/api/content';

let landingFeatures = $state<LandingFeature[]>([]);
let loaded = $state(false);

export async function initContent(force = false) {
	if (loaded && !force) return;
	if (!(await apiHealth())) return;
	try {
		const data = await fetchLandingContent();
		landingFeatures = (data.payload.features ?? []) as LandingFeature[];
		loaded = true;
	} catch (err) {
		console.error('Landing content load failed:', err);
	}
}

export function getLandingFeatures(): LandingFeature[] {
	return landingFeatures;
}

