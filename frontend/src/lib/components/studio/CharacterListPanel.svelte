<script lang="ts">
	import type { Character } from '$lib/data/mock';
	import { Plus, Search } from 'lucide-svelte';

	interface Props {
		characters: Character[];
		selectedId: string;
		onselect: (id: string) => void;
	}

	let { characters, selectedId, onselect }: Props = $props();
	let query = $state('');

	const filtered = $derived(
		characters.filter(
			(c) =>
				!query ||
				c.name.includes(query) ||
				c.world.includes(query) ||
				c.title.includes(query)
		)
	);
</script>

<aside class="flex w-64 shrink-0 flex-col border-r border-white/10 bg-bg-surface/40">
	<div class="border-b border-white/10 p-4">
		<div class="mb-3 flex items-center justify-between">
			<h2 class="text-sm font-semibold">캐릭터 목록</h2>
			<span class="text-xs text-text-muted">{characters.length} / 50</span>
		</div>
		<div class="flex gap-2">
			<div class="relative flex-1">
				<Search class="absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-text-muted" />
				<input
					type="search"
					placeholder="검색..."
					bind:value={query}
					class="h-9 w-full rounded-lg border border-white/10 bg-bg-primary/60 pl-9 pr-3 text-xs outline-none focus:border-primary-500"
				/>
			</div>
			<button
				type="button"
				class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-white/10 bg-primary-600/20 text-primary-300 hover:bg-primary-600/30"
				aria-label="새 캐릭터"
			>
				<Plus class="h-4 w-4" />
			</button>
		</div>
	</div>

	<div class="flex-1 space-y-1 overflow-y-auto p-2">
		{#each filtered as char (char.id)}
			<button
				type="button"
				onclick={() => onselect(char.id)}
				class="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left transition {selectedId ===
				char.id
					? 'bg-primary-600/20 ring-1 ring-primary-500/40'
					: 'hover:bg-white/5'}"
			>
				<img src={char.avatar} alt="" class="h-10 w-10 rounded-full bg-bg-card object-cover" />
				<div class="min-w-0 flex-1">
					<p class="truncate text-sm font-medium">{char.name}</p>
					<p class="truncate text-[10px] text-text-muted">{char.worldName}</p>
				</div>
			</button>
		{/each}
	</div>
</aside>
