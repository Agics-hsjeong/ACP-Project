<script lang="ts">
	import { page } from '$app/stores';
	import MobileShell from '$lib/components/layout/MobileShell.svelte';

	let { children }: { children: import('svelte').Snippet } = $props();
	const isShowcase = $derived($page.url.pathname === '/mobile');
</script>

{#if isShowcase}
	{@render children()}
{:else}
	<div class="min-h-screen bg-gradient-to-b from-bg-primary to-primary-950/30 p-4 lg:flex lg:items-start lg:justify-center lg:p-8">
		<MobileShell>{@render children()}</MobileShell>
	</div>
{/if}
