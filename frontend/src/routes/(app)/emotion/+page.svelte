<script lang="ts">
	import EmotionRadar from '$lib/components/emotion/EmotionRadar.svelte';
	import EmotionTrendChart from '$lib/components/emotion/EmotionTrendChart.svelte';
	import EmotionScoreCard from '$lib/components/emotion/EmotionScoreCard.svelte';
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import { getEmotions, getEmotionTrend, initEmotionApi } from '$lib/stores/emotion.svelte';
	import { getCatalogCharacters } from '$lib/stores/catalog.svelte';
	import { Sparkles } from 'lucide-svelte';

	const characters = $derived(getCatalogCharacters());
	const emotions = $derived(getEmotions());
	const emotionTrend = $derived(getEmotionTrend());

	let characterId = $state('elia');
	let period = $state<'7' | '30' | '90' | 'all'>('30');

	const activeCharacter = $derived(characters.find((c) => c.id === characterId));

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
			? emotions.map((e) => ({ ...e, color: emotionColors[e.key] ?? e.color }))
			: [
					{ key: 'trust', label: '신뢰', value: 72, color: '#4d80f2' },
					{ key: 'affection', label: '애정', value: 85, color: '#f26699' },
					{ key: 'respect', label: '존경', value: 64, color: '#33b266' },
					{ key: 'jealousy', label: '질투', value: 18, color: '#994de5' },
					{ key: 'anger', label: '분노', value: 12, color: '#f28033' },
					{ key: 'fear', label: '공포', value: 8, color: '#808080' }
				]
	);

	const trends = [2.4, -1.2, 0.8, -0.5, 1.1, -0.3];

	const slicedTrend = $derived.by(() => {
		const base = emotionTrend.length
			? emotionTrend
			: Array.from({ length: 14 }, (_, i) => ({
					day: i + 1,
					affection: 70 + Math.sin(i * 0.5) * 10,
					trust: 65 + Math.cos(i * 0.4) * 8,
					anger: 15 + Math.sin(i * 0.3) * 5
				}));
		const days = period === '7' ? 7 : period === '30' ? 30 : period === '90' ? 90 : base.length;
		return base.slice(-days);
	});

	const distribution = $derived(
		displayEmotions.map((e) => ({
			label: e.label,
			color: e.color,
			pct: Math.round((e.value / displayEmotions.reduce((s, x) => s + x.value, 0)) * 100)
		}))
	);

	const insight = $derived.by(() => {
		if (!displayEmotions.length) return '감정 데이터를 불러오는 중입니다.';
		const affection = displayEmotions.find((e) => e.key === 'affection')?.value ?? 0;
		const trust = displayEmotions.find((e) => e.key === 'trust')?.value ?? 0;
		const anger = displayEmotions.find((e) => e.key === 'anger')?.value ?? 0;
		if (affection > 70 && trust > 65)
			return `${activeCharacter?.name ?? '캐릭터'}와의 관계에서 애정(${Math.round(affection)})과 신뢰(${Math.round(trust)})가 높은 수준을 유지하고 있습니다. 긍정적인 대화 패턴이 지속되고 있어요.`;
		if (anger > 50)
			return `분노 지수가 ${Math.round(anger)}로 상승했습니다. 최근 갈등 이벤트가 감정에 영향을 미쳤을 수 있어요.`;
		const top = [...displayEmotions].sort((a, b) => b.value - a.value)[0];
		return `${top?.label ?? '감정'}이 현재 가장 두드러진 축입니다. 대화 톤과 상호작용을 통해 6축 감정이 실시간으로 변화합니다.`;
	});

	$effect(() => {
		void initEmotionApi(characterId);
	});
</script>

<svelte:head>
	<title>감정 분석 — ACP</title>
</svelte:head>

<div class="mb-6 flex flex-wrap items-center justify-between gap-4">
	<div>
		<h1 class="text-2xl font-bold">감정 분석 대시보드</h1>
		<p class="mt-1 text-sm text-text-muted">6축 감정 시스템 — 관계 심층 분석</p>
	</div>
	<div class="flex flex-wrap items-center gap-2">
		<select
			bind:value={characterId}
			class="h-9 rounded-xl border border-[#333847] bg-[#1a1c26] px-3 text-sm outline-none focus:border-[#8c5cfa]"
		>
			{#each characters as c}
				<option value={c.id}>{c.name}</option>
			{/each}
		</select>
		<div class="flex gap-1 rounded-xl border border-[#333847] bg-[#1a1c26] p-1">
			{#each [
				{ key: '7', label: '7일' },
				{ key: '30', label: '30일' },
				{ key: '90', label: '90일' },
				{ key: 'all', label: '전체' }
			] as p}
				<button
					type="button"
					class="rounded-lg px-3 py-1.5 text-xs font-medium transition {period === p.key
						? 'bg-[#8c5cfa] text-white'
						: 'text-text-muted hover:text-text-primary'}"
					onclick={() => (period = p.key as typeof period)}
				>
					{p.label}
				</button>
			{/each}
		</div>
	</div>
</div>

<div class="mb-5 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
	{#each displayEmotions as emo, i}
		<EmotionScoreCard
			value={emo.value}
			label={emo.label}
			color={emo.color}
			trend={trends[i % trends.length]}
		/>
	{/each}
</div>

<div class="mb-5 grid gap-4 lg:grid-cols-3">
	<MockPanel class="lg:col-span-2">
		<div class="mb-4 flex items-center justify-between">
			<h2 class="font-semibold">감정 변화 추이</h2>
			<span class="text-xs text-text-muted">
				{period === 'all' ? '전체' : `${period}일`}
			</span>
		</div>
		<EmotionTrendChart data={slicedTrend} height={220} />
	</MockPanel>

	<MockPanel>
		<div class="mb-3 flex items-center gap-2">
			<Sparkles class="h-4 w-4 text-[#8c5cfa]" />
			<h2 class="font-semibold">AI 인사이트</h2>
		</div>
		<p class="text-sm leading-relaxed text-text-secondary">{insight}</p>
	</MockPanel>
</div>

<div class="grid gap-4 lg:grid-cols-3">
	<MockPanel>
		<h2 class="mb-4 font-semibold">감정 분포</h2>
		<div class="flex items-center gap-4">
			<div
				class="relative mx-auto flex h-32 w-32 shrink-0 items-center justify-center rounded-full border-4 border-[#262933]"
				aria-hidden="true"
			>
				<div
					class="absolute inset-2 rounded-full"
					style="background: conic-gradient(
						#f26699 0% {distribution[1]?.pct ?? 25}%,
						#4d80f2 {distribution[1]?.pct ?? 25}% {(distribution[1]?.pct ?? 25) + (distribution[0]?.pct ?? 20)}%,
						#33b266 {(distribution[1]?.pct ?? 25) + (distribution[0]?.pct ?? 20)}% {(distribution[1]?.pct ?? 25) + (distribution[0]?.pct ?? 20) + (distribution[2]?.pct ?? 15)}%,
						#994de5 {(distribution[1]?.pct ?? 25) + (distribution[0]?.pct ?? 20) + (distribution[2]?.pct ?? 15)}% 100%
					)"
				></div>
				<span class="relative text-lg font-bold">100%</span>
			</div>
			<div class="space-y-1.5">
				{#each distribution as d}
					<p class="flex items-center gap-2 text-xs text-text-secondary">
						<span class="h-2 w-2 rounded-full" style="background: {d.color}"></span>
						{d.label}
						<span class="ml-auto text-text-muted">{d.pct}%</span>
					</p>
				{/each}
			</div>
		</div>
	</MockPanel>

	<MockPanel>
		<h2 class="mb-4 font-semibold">히트맵</h2>
		<div class="grid grid-cols-7 gap-1">
			{#each Array(28) as _, i}
				{@const intensity = (i * 17 + 23) % 100}
				<div
					class="aspect-square rounded-sm"
					style="background: rgba(140, 92, 250, {0.15 + (intensity / 100) * 0.7})"
					title="Day {i + 1}"
				></div>
			{/each}
		</div>
		<p class="mt-3 text-center text-[10px] text-text-muted">최근 4주 감정 강도</p>
	</MockPanel>

	<MockPanel>
		<h2 class="mb-4 font-semibold">균형도</h2>
		<EmotionRadar emotions={displayEmotions} size={200} />
	</MockPanel>
</div>
