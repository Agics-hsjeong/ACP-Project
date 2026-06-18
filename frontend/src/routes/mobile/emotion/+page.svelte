<script lang="ts">
	import EmotionRadar from '$lib/components/emotion/EmotionRadar.svelte';
	import EmotionTrendChart from '$lib/components/emotion/EmotionTrendChart.svelte';
	import EmotionBars from '$lib/components/emotion/EmotionBars.svelte';
	import { getEmotions, getEmotionTrend, initEmotionApi } from '$lib/stores/emotion.svelte';
	import { getCatalogCharacters } from '$lib/stores/catalog.svelte';

	const emotions = $derived(getEmotions());
	const emotionTrend = $derived(getEmotionTrend());
	const characters = $derived(getCatalogCharacters());

	let characterId = $state('elia');

	const activeCharacter = $derived(characters.find((c) => c.id === characterId));

	$effect(() => {
		void initEmotionApi(characterId);
	});
</script>

<svelte:head>
	<title>감정 분석 — Mobile</title>
</svelte:head>

<div class="border-b border-white/10 p-4">
	<h1 class="text-lg font-bold">감정 분석</h1>
	<p class="text-xs text-text-muted">{activeCharacter?.name ?? '캐릭터'} · 6축 감정</p>
	<select
		bind:value={characterId}
		class="mt-2 h-9 w-full rounded-lg border border-white/10 bg-bg-primary/60 px-3 text-xs outline-none focus:border-primary-500"
	>
		{#each characters as c}
			<option value={c.id}>{c.name}</option>
		{/each}
	</select>
</div>

<div class="space-y-4 p-4">
	<section class="rounded-xl border border-white/10 bg-bg-surface/50 p-4">
		<h2 class="mb-3 text-sm font-semibold">감정 레이더</h2>
		<EmotionRadar {emotions} size={200} />
	</section>
	<section class="rounded-xl border border-white/10 bg-bg-surface/50 p-4">
		<h2 class="mb-3 text-sm font-semibold">30일 추이</h2>
		<EmotionTrendChart data={emotionTrend} />
	</section>
	<section class="rounded-xl border border-white/10 bg-bg-surface/50 p-4">
		<h2 class="mb-3 text-sm font-semibold">상세 수치</h2>
		<EmotionBars {emotions} compact />
	</section>
</div>
