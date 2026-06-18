<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import { getCatalogWorlds } from '$lib/stores/catalog.svelte';
	import { getExploreTags } from '$lib/stores/meta.svelte';
	import { RotateCcw } from 'lucide-svelte';

	interface Props {
		sort?: string;
		gender?: string;
		world?: string;
		selectedTags?: string[];
		onSearch?: () => void;
	}

	let {
		sort = $bindable('popular'),
		gender = $bindable('all'),
		world = $bindable('all'),
		selectedTags = $bindable([] as string[]),
		onSearch
	}: Props = $props();

	const exploreTags = $derived(getExploreTags());
	const worlds = $derived(getCatalogWorlds());

	const activeCount = $derived(
		(sort !== 'popular' ? 1 : 0) +
			(gender !== 'all' ? 1 : 0) +
			(world !== 'all' ? 1 : 0) +
			selectedTags.length
	);

	function toggleTag(tag: string) {
		selectedTags = selectedTags.includes(tag)
			? selectedTags.filter((t) => t !== tag)
			: [...selectedTags, tag];
	}

	function resetFilters() {
		sort = 'popular';
		gender = 'all';
		world = 'all';
		selectedTags = [];
	}
</script>

<aside class="space-y-5 rounded-2xl border border-white/10 bg-bg-surface/60 p-5">
	<div class="flex items-center justify-between">
		<h3 class="font-semibold">상세 필터</h3>
		{#if activeCount > 0}
			<span class="rounded-full bg-primary-500/20 px-2 py-0.5 text-[10px] text-primary-300">
				{activeCount}개 적용
			</span>
		{/if}
	</div>

	<div>
		<label for="sort" class="mb-1.5 block text-xs text-text-muted">정렬</label>
		<select
			id="sort"
			bind:value={sort}
			class="h-10 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none focus:border-primary-500"
		>
			<option value="popular">인기순</option>
			<option value="latest">최신순</option>
			<option value="likes">호감도순</option>
		</select>
	</div>

	<div>
		<p class="mb-2 text-xs text-text-muted">세계관</p>
		<div class="flex flex-wrap gap-2">
			<button
				class="rounded-lg px-3 py-1.5 text-xs transition {world === 'all'
					? 'bg-primary-600 text-white'
					: 'bg-bg-card/60 text-text-secondary hover:bg-bg-card'}"
				onclick={() => (world = 'all')}
			>
				전체
			</button>
			{#each worlds as w}
				<button
					class="rounded-lg px-3 py-1.5 text-xs transition {world === w.id
						? 'bg-primary-600 text-white'
						: 'bg-bg-card/60 text-text-secondary hover:bg-bg-card'}"
					onclick={() => (world = w.id)}
				>
					{w.name}
				</button>
			{/each}
		</div>
	</div>

	<div>
		<p class="mb-2 text-xs text-text-muted">성별</p>
		<div class="flex flex-wrap gap-2">
			{#each [
				{ id: 'all', label: '전체' },
				{ id: 'female', label: '여성' },
				{ id: 'male', label: '남성' }
			] as g}
				<button
					class="rounded-lg px-3 py-1.5 text-xs transition {gender === g.id
						? 'bg-primary-600 text-white'
						: 'bg-bg-card/60 text-text-secondary hover:bg-bg-card'}"
					onclick={() => (gender = g.id)}
				>
					{g.label}
				</button>
			{/each}
		</div>
	</div>

	<div>
		<p class="mb-2 text-xs text-text-muted">태그</p>
		<div class="flex flex-wrap gap-1.5">
			{#each exploreTags as tag}
				<button
					class="rounded-md px-2 py-1 text-[11px] transition {selectedTags.includes(tag)
						? 'bg-primary-500/30 text-primary-200'
						: 'bg-bg-card/50 text-text-muted hover:text-text-secondary'}"
					onclick={() => toggleTag(tag)}
				>
					#{tag}
				</button>
			{/each}
		</div>
	</div>

	<div class="flex gap-2">
		<Button variant="ghost" class="flex-1" onclick={resetFilters}>
			<RotateCcw class="h-3.5 w-3.5" />
			초기화
		</Button>
		<Button class="flex-1" onclick={onSearch}>검색</Button>
	</div>
</aside>
