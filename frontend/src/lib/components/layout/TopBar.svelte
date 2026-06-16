<script lang="ts">
	import { goto } from '$app/navigation';
	import { getSearchQuery, setSearchQuery } from '$lib/stores/search.svelte';
	import { Bell, Mail } from 'lucide-svelte';
	import SearchBar from '$lib/components/ui/SearchBar.svelte';

	interface Props {
		title?: string;
	}

	let { title }: Props = $props();
	let query = $state(getSearchQuery());

	function submitSearch() {
		const value = query.trim();
		setSearchQuery(value);
		goto(value ? `/explore?q=${encodeURIComponent(value)}` : '/explore');
	}
</script>

<header class="flex items-center gap-4 border-b border-white/10 bg-bg-primary/80 px-6 py-4 backdrop-blur-sm">
	{#if title}
		<h1 class="shrink-0 text-lg font-semibold">{title}</h1>
	{/if}
	<form class="max-w-xl flex-1" onsubmit={(e) => { e.preventDefault(); submitSearch(); }}>
		<SearchBar bind:value={query} placeholder="캐릭터·세계관 검색..." />
	</form>
	<div class="ml-auto flex items-center gap-2">
		<button type="button" class="relative rounded-lg p-2 text-text-secondary hover:bg-white/5 hover:text-text-primary" aria-label="알림">
			<Bell class="h-5 w-5" />
			<span class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-accent-red"></span>
		</button>
		<button type="button" class="rounded-lg p-2 text-text-secondary hover:bg-white/5 hover:text-text-primary" aria-label="메시지">
			<Mail class="h-5 w-5" />
		</button>
		<a href="/mypage" class="ml-2 flex h-9 w-9 items-center justify-center rounded-full bg-primary-600 text-sm font-medium">
			C
		</a>
	</div>
</header>
