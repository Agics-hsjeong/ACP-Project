<script lang="ts">
	import { page } from '$app/stores';
	import SideNav from './SideNav.svelte';
	import TopBar from './TopBar.svelte';
	import MobileNav from './MobileNav.svelte';

	let { children }: { children: import('svelte').Snippet } = $props();

	const isChat = $derived($page.url.pathname.startsWith('/chat'));
	const isGraph = $derived($page.url.pathname.startsWith('/relationship'));
	const isStudio = $derived($page.url.pathname.startsWith('/studio'));
	const hideTopBar = $derived(isChat || isGraph || isStudio);
	const isFullscreen = $derived(isChat || isGraph || isStudio);
</script>

<div class="flex min-h-screen bg-bg-primary">
	<div class="hidden lg:flex">
		<SideNav />
	</div>
	<div class="flex min-w-0 flex-1 flex-col">
		{#if !hideTopBar}
			<TopBar />
		{/if}
		<main
			class="flex-1 {isFullscreen
				? 'overflow-hidden'
				: 'overflow-y-auto p-4 pb-20 lg:p-6 lg:pb-6'}"
		>
			{@render children()}
		</main>
	</div>
	<MobileNav />
</div>
