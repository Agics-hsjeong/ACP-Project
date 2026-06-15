<script lang="ts">
	import { Bell, Mail } from 'lucide-svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';

	interface Props {
		title?: string;
	}

	let { title }: Props = $props();
	let query = $state('');
</script>

<header class="flex items-center gap-4 border-b border-white/10 bg-bg-primary/80 px-6 py-4 backdrop-blur-sm">
	{#if title}
		<h1 class="shrink-0 text-lg font-semibold">{title}</h1>
	{/if}
	<SearchBar bind:value={query} class="max-w-xl flex-1" />
	<div class="ml-auto flex items-center gap-2">
		<button class="rounded-lg p-2 text-text-secondary hover:bg-white/5 hover:text-text-primary" aria-label="알림">
			<Bell class="h-5 w-5" />
		</button>
		<button class="rounded-lg p-2 text-text-secondary hover:bg-white/5 hover:text-text-primary" aria-label="메시지">
			<Mail class="h-5 w-5" />
		</button>
		<div class="ml-2 flex h-9 w-9 items-center justify-center rounded-full bg-primary-600 text-sm font-medium">
			C
		</div>
	</div>
</header>
