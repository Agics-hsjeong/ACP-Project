<script lang="ts">
	import type { Memory } from '$lib/data/mock';

	interface TagItem {
		tag: string;
		count: number;
	}

	interface Props {
		tags: TagItem[];
		memories: Memory[];
		activeTag?: string;
		onselect?: (tag: string) => void;
	}

	let { tags, memories, activeTag = '', onselect }: Props = $props();
</script>

<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-5">
	<h3 class="mb-4 text-sm font-semibold">Top 5 태그</h3>
	<div class="space-y-2">
		{#each tags as item}
			<button
				type="button"
				onclick={() => onselect?.(item.tag)}
				class="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left text-sm transition {activeTag ===
				item.tag
					? 'bg-primary-600/20 text-primary-300'
					: 'hover:bg-white/5'}"
			>
				<span class="flex-1">{item.tag}</span>
				<span class="text-xs text-text-muted">{item.count}</span>
				<div class="h-1.5 w-16 overflow-hidden rounded-full bg-bg-primary">
					<div
						class="h-full rounded-full bg-primary-500"
						style="width: {(item.count / tags[0].count) * 100}%"
					></div>
				</div>
			</button>
		{/each}
	</div>
	<p class="mt-4 text-xs text-text-muted">
		총 {memories.length}개의 기억에서 추출된 태그입니다.
	</p>
</div>
