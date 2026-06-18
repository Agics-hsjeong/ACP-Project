<script lang="ts">
	import MockPanel from './MockPanel.svelte';
	import { getExploreTags } from '$lib/stores/meta.svelte';

	interface Props {
		selectedTags?: string[];
		ontagclick?: (tag: string) => void;
	}

	let { selectedTags = [], ontagclick }: Props = $props();

	const exploreTags = $derived(getExploreTags());

	const tips = [
		'태그를 클릭하면 관련 캐릭터를 빠르게 찾을 수 있어요',
		'세계관 필터로 원하는 배경의 캐릭터만 볼 수 있습니다',
		'인기순·최신순·호감도순으로 정렬해 보세요'
	];
</script>

<aside class="sticky top-6 w-[370px] shrink-0 space-y-4 self-start">
	<MockPanel title="탐색 도움말">
		<p class="mb-4 text-xs leading-relaxed text-text-muted">
			원하는 캐릭터를 더 쉽게 찾기 위한 팁과 인기 태그입니다.
		</p>
		<ul class="mb-5 space-y-2">
			{#each tips as tip}
				<li class="flex gap-2 text-[11px] leading-relaxed text-text-secondary">
					<span class="mt-1 h-1 w-1 shrink-0 rounded-full bg-mock-accent"></span>
					{tip}
				</li>
			{/each}
		</ul>
		<p class="mb-2.5 text-xs font-medium text-text-secondary">인기 태그</p>
		<div class="flex flex-wrap gap-1.5">
			{#each exploreTags as tag}
				<button
					type="button"
					class="rounded-md border px-2.5 py-1 text-[11px] transition {selectedTags.includes(tag)
						? 'border-mock-accent/50 bg-mock-accent/15 text-mock-accent'
						: 'border-mock-border bg-mock-bg/60 text-text-muted hover:border-mock-accent/30 hover:text-text-secondary'}"
					onclick={() => ontagclick?.(tag)}
				>
					#{tag}
				</button>
			{:else}
				<p class="text-[11px] text-text-muted">태그를 불러오는 중…</p>
			{/each}
		</div>
	</MockPanel>
</aside>
