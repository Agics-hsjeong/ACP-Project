<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import { exploreTags } from '$lib/data/mock';

	interface Props {
		sort?: string;
		gender?: string;
		selectedTags?: string[];
		onSearch?: () => void;
	}

	let {
		sort = $bindable('popular'),
		gender = $bindable('all'),
		selectedTags = $bindable([] as string[]),
		onSearch
	}: Props = $props();

	function toggleTag(tag: string) {
		selectedTags = selectedTags.includes(tag)
			? selectedTags.filter((t) => t !== tag)
			: [...selectedTags, tag];
	}
</script>

<aside class="sticky top-6 space-y-5 rounded-2xl border border-white/10 bg-bg-surface/60 p-5">
	<h3 class="font-semibold">상세 필터</h3>

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

	<Button fullWidth onclick={onSearch}>검색</Button>
</aside>
