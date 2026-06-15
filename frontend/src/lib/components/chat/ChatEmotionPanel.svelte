<script lang="ts">
	import EmotionBars from '$lib/components/emotion/EmotionBars.svelte';
	import IntimacyGauge from '$lib/components/emotion/IntimacyGauge.svelte';
	import RelationshipMiniGraph from '$lib/components/relationship/RelationshipMiniGraph.svelte';
	import { getEmotions, getIntimacy } from '$lib/stores/emotion.svelte';

	interface Props {
		intimacy?: number;
		characterId?: string;
	}

	let { characterId = 'elia' }: Props = $props();

	const emotions = $derived(getEmotions());
	const intimacy = $derived(getIntimacy());
</script>

<aside class="hidden w-72 shrink-0 flex-col border-l border-white/10 bg-bg-surface/30 xl:flex">
	<div class="border-b border-white/10 p-5">
		<h3 class="mb-4 text-sm font-semibold">감정 상태</h3>
		<IntimacyGauge value={intimacy} label="매우 가까운 관계" />
		<p class="mt-3 text-center text-xs text-text-muted">실시간 감정 · 6축</p>
	</div>

	<div class="flex-1 overflow-y-auto p-5">
		<EmotionBars {emotions} compact />

		<div class="mt-6">
			<p class="mb-2 text-xs font-medium text-text-secondary">관계 미니맵</p>
			{#key characterId}
				<RelationshipMiniGraph centerId={characterId} />
			{/key}
			<a href="/relationship" class="mt-2 block text-center text-[10px] text-primary-400 hover:underline">
				전체 관계도 보기 →
			</a>
		</div>
	</div>
</aside>
