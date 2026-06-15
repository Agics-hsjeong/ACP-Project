<script lang="ts">
	import EmotionRadar from '$lib/components/emotion/EmotionRadar.svelte';
	import EmotionTrendChart from '$lib/components/emotion/EmotionTrendChart.svelte';
	import EmotionBars from '$lib/components/emotion/EmotionBars.svelte';
	import IntimacyGauge from '$lib/components/emotion/IntimacyGauge.svelte';
	import { emotions, emotionTrend } from '$lib/data/mock';
</script>

<svelte:head>
	<title>감정 분석 — ACP</title>
</svelte:head>

<div class="mb-6">
	<h1 class="text-2xl font-bold">감정 분석 대시보드</h1>
	<p class="mt-1 text-sm text-text-muted">6축 감정 시스템 — 엘리아와의 관계</p>
</div>

<div class="mb-6 grid gap-4 sm:grid-cols-3">
	<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6 sm:col-span-1">
		<IntimacyGauge value={82} label="매우 가까운 관계" />
	</div>
	<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6 sm:col-span-2">
		<h2 class="mb-4 font-semibold">감정 상태</h2>
		<EmotionBars {emotions} />
	</div>
</div>

<div class="grid gap-6 lg:grid-cols-2">
	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="mb-4 font-semibold">감정 레이더</h2>
		<EmotionRadar {emotions} />
	</section>

	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<div class="mb-4 flex items-center justify-between">
			<h2 class="font-semibold">실시간 감정 변화</h2>
			<select class="rounded-lg border border-white/10 bg-bg-primary/60 px-2 py-1 text-xs">
				<option>최근 14일</option>
				<option>최근 30일</option>
			</select>
		</div>
		<EmotionTrendChart data={emotionTrend} height={160} />
		<p class="mt-2 text-xs text-text-muted">※ 고급 히트맵·AI 인사이트는 Phase 3</p>
	</section>
</div>

<section class="mt-6 rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
	<h2 class="mb-2 font-semibold">AI 인사이트</h2>
	<p class="text-sm text-text-secondary">
		최근 2주간 <span class="text-accent-pink">애정</span>과
		<span class="text-primary-400">신뢰</span>가 꾸준히 상승했습니다. 달빛 아래의 대화와 정원에서의
		첫 만남이 관계 형성에 핵심적인 역할을 했어요.
	</p>
</section>
