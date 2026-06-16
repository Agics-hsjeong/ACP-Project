<script lang="ts">
	import { onMount } from 'svelte';
	import type { Snippet } from 'svelte';
	import AppShell from '$lib/components/layout/AppShell.svelte';
	import { initCatalog } from '$lib/stores/catalog.svelte';
	import { initEmotionApi } from '$lib/stores/emotion.svelte';

	let { children }: { children: Snippet } = $props();

	onMount(() => {
		void initCatalog();
		void initEmotionApi('elia');
	});
</script>

<AppShell>
	{@render children()}
</AppShell>
