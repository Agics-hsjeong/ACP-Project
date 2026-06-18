<script lang="ts">
	import RelationshipMiniGraph from '$lib/components/relationship/RelationshipMiniGraph.svelte';
	import { getEmotions, getIntimacy, initEmotionApi } from '$lib/stores/emotion.svelte';
	import { getEliaRelationships, initRelationship } from '$lib/stores/relationship.svelte';
	import { edgeStyles } from '$lib/data/relationship';

	interface Props {
		characterId?: string;
	}

	let { characterId = 'elia' }: Props = $props();

	const emotions = $derived(getEmotions());
	const intimacy = $derived(getIntimacy());
	const relations = $derived(getEliaRelationships());

	const emotionColors: Record<string, string> = {
		trust: '#4d80f2',
		affection: '#f26699',
		respect: '#33b266',
		jealousy: '#994de5',
		anger: '#f28033',
		fear: '#808080'
	};

	const displayEmotions = $derived(
		emotions.length
			? emotions.map((e) => ({
					...e,
					color: emotionColors[e.key] ?? e.color
				}))
			: [
					{ key: 'trust', label: '신뢰', value: 72, color: '#4d80f2' },
					{ key: 'affection', label: '애정', value: 85, color: '#f26699' },
					{ key: 'respect', label: '존경', value: 64, color: '#33b266' },
					{ key: 'jealousy', label: '질투', value: 18, color: '#994de5' },
					{ key: 'anger', label: '분노', value: 12, color: '#f28033' },
					{ key: 'fear', label: '공포', value: 8, color: '#808080' }
				]
	);

	$effect(() => {
		void initEmotionApi(characterId);
		void initRelationship({ center: characterId });
	});
</script>

<aside class="hidden w-[450px] shrink-0 flex-col border-l border-[#333847] bg-[#0a0a14] lg:flex">
	<div class="flex-1 overflow-y-auto p-5">
		<h3 class="text-sm font-semibold text-text-primary">감정 상태</h3>

		<div class="mt-5 mb-8">
			<p class="text-5xl font-bold leading-none tracking-tight text-[#8c5cfa]">
				{Math.round(intimacy || 82)}
			</p>
			<p class="mt-1 text-sm text-text-muted">친밀도</p>
		</div>

		<div class="space-y-4">
			{#each displayEmotions as emo}
				<div>
					<div class="mb-1.5 flex items-center justify-between text-xs">
						<span class="text-text-secondary">{emo.label}</span>
						<span class="font-medium" style="color: {emo.color}">{Math.round(emo.value)}</span>
					</div>
					<div class="h-1 overflow-hidden rounded-full bg-[#262933]">
						<div
							class="h-full rounded-full transition-all"
							style="width: {emo.value}%; background: {emo.color}"
						></div>
					</div>
				</div>
			{/each}
		</div>

		<section class="mt-8">
			<h4 class="mb-3 text-sm font-semibold">관계도</h4>
			{#key characterId}
				<RelationshipMiniGraph centerId={characterId} />
			{/key}
			<div class="mt-3 space-y-1.5">
				{#each relations.slice(0, 4) as rel}
					<p class="flex items-center gap-2 text-xs text-text-secondary">
						<span
							class="h-1.5 w-1.5 shrink-0 rounded-full"
							style="background: {edgeStyles[rel.type].color}"
						></span>
						<span class="truncate">{rel.name}</span>
						<span class="ml-auto shrink-0 text-text-muted">{rel.score}</span>
					</p>
				{/each}
			</div>
			<a href="/relationship" class="mt-3 block text-center text-[11px] text-[#8c5cfa] hover:underline">
				전체 관계도 보기 →
			</a>
		</section>
	</div>
</aside>
