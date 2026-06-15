<script lang="ts">
	import type { Memory } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { MessageCircle } from 'lucide-svelte';

	interface Props {
		memory: Memory | null;
	}

	let { memory }: Props = $props();
</script>

<aside class="sticky top-6 hidden w-80 shrink-0 xl:block">
	{#if memory}
		<div class="rounded-2xl border border-white/10 bg-bg-surface/60 p-5">
			<div class="mb-4 aspect-[3/4] overflow-hidden rounded-xl bg-bg-card">
				<img
					src={memory.thumbnail ?? `https://api.dicebear.com/9.x/shapes/svg?seed=${memory.id}`}
					alt=""
					class="h-full w-full object-cover"
				/>
			</div>
			<Badge
				label={memory.importance === 'high' ? '중요한 순간' : '일반 기억'}
				variant={memory.importance === 'high' ? 'accent' : 'default'}
			/>
			<h3 class="mt-3 text-lg font-bold">{memory.title}</h3>
			<p class="mt-1 text-xs text-text-muted">{memory.date} · {memory.location ?? '—'}</p>
			<p class="mt-4 text-sm leading-relaxed text-text-secondary">{memory.detail ?? memory.summary}</p>
			{#if memory.quote}
				<blockquote class="mt-4 border-l-2 border-primary-500 pl-3 text-sm italic text-primary-200">
					{memory.quote}
				</blockquote>
			{/if}
			{#if memory.stats}
				<div class="mt-4 space-y-2">
					<p class="text-xs font-medium text-text-muted">관계 영향</p>
					{#each Object.entries(memory.stats) as [key, val]}
						{#if val}
							<p class="text-sm text-accent-green">
								{key === 'affection' ? '애정' : key === 'trust' ? '신뢰' : '존경'} +{val}
							</p>
						{/if}
					{/each}
				</div>
			{/if}
			<Button href="/chat/{memory.characterId ?? 'elia'}" fullWidth class="mt-5" size="sm">
				<MessageCircle class="h-4 w-4" />
				이 기억의 대화 보기
			</Button>
		</div>
	{:else}
		<div class="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-text-muted">
			기억을 선택하면 상세 정보가 표시됩니다
		</div>
	{/if}
</aside>
