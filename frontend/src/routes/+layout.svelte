<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { onMount } from 'svelte';
	import { initCatalog } from '$lib/stores/catalog.svelte';
	import { initContent } from '$lib/stores/content.svelte';
	import { initMeta } from '$lib/stores/meta.svelte';
	import { initRelationship } from '$lib/stores/relationship.svelte';
	import { initStudio } from '$lib/stores/studio.svelte';

	let { children } = $props();

	onMount(() => {
		void initCatalog();
		void initContent();
		void initMeta();
		void initRelationship({ center: 'elia' });
		void initStudio();
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>AI Character Playground</title>
</svelte:head>

{@render children()}
