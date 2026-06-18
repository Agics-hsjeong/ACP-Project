<script lang="ts">
	import { onMount } from 'svelte';
	import type { Snippet } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import AppShell from '$lib/components/layout/AppShell.svelte';
	import { isGuestAllowedPath, getLoginUrl } from '$lib/auth/access';
	import { initCatalog, isCatalogLoaded, refreshPrivateCatalogData } from '$lib/stores/catalog.svelte';
	import { initEmotionApi } from '$lib/stores/emotion.svelte';
	import { isLoggedIn, restoreSession } from '$lib/stores/auth.svelte';

	let { children }: { children: Snippet } = $props();
	let sessionReady = $state(false);

	onMount(async () => {
		await restoreSession();
		sessionReady = true;
		if (!isCatalogLoaded()) {
			await initCatalog();
		}
		if (isLoggedIn()) {
			await refreshPrivateCatalogData();
			void initEmotionApi('elia');
		}
	});

	$effect(() => {
		if (!browser || !sessionReady) return;
		const path = $page.url.pathname;
		if (!isLoggedIn() && !isGuestAllowedPath(path)) {
			void goto(getLoginUrl(path), { replaceState: true });
		}
	});
</script>

<AppShell>
	{@render children()}
</AppShell>
