<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import {
		arcadiaWorld,
		worldFactions,
		worldThemes,
		worldEras,
		worldLaws,
		worldEvents,
		worldStudioTabs,
		studioWorlds,
		type WorldTab
	} from '$lib/data/studio';
	import { Check, Eye, Map, Pencil, Plus } from 'lucide-svelte';

	let activeTab = $state<WorldTab>('overview');
	let selectedWorldId = $state('arcadia');
	let saved = $state(true);

	const world = $derived(
		studioWorlds.find((w) => w.id === selectedWorldId) ?? studioWorlds[0]
	);
</script>

<svelte:head>
	<title>세계관 스튜디오 — ACP</title>
</svelte:head>

<div class="flex h-[calc(100dvh-0px)] min-h-[600px] flex-col lg:h-[calc(100vh-0px)]">
	<header class="flex flex-wrap items-center gap-3 border-b border-white/10 px-4 py-3">
		<div class="flex items-center gap-2">
			<div>
				<p class="text-xs text-text-muted">세계관 스튜디오 › {arcadiaWorld.name}</p>
				<h1 class="flex items-center gap-2 text-lg font-bold">
					{arcadiaWorld.name}
					<button type="button" class="text-text-muted hover:text-primary-300" aria-label="이름 편집">
						<Pencil class="h-4 w-4" />
					</button>
				</h1>
			</div>
		</div>
		<div class="ml-auto flex flex-wrap items-center gap-2">
			{#if saved}
				<span class="flex items-center gap-1 text-xs text-accent-green">
					<Check class="h-3.5 w-3.5" /> 저장됨
				</span>
			{/if}
			<Button variant="secondary" class="gap-2">
				<Eye class="h-4 w-4" /> 미리보기
			</Button>
			<Button onclick={() => (saved = true)}>저장하기</Button>
		</div>
	</header>

	<nav class="flex gap-1 overflow-x-auto border-b border-white/10 px-4">
		{#each worldStudioTabs as tab}
			<button
				type="button"
				onclick={() => (activeTab = tab.id)}
				class="shrink-0 border-b-2 px-4 py-3 text-sm transition {activeTab === tab.id
					? 'border-primary-500 text-primary-300'
					: 'border-transparent text-text-muted hover:text-text-primary'}"
			>
				{tab.label}
			</button>
		{/each}
	</nav>

	<div class="flex-1 overflow-y-auto p-4 lg:p-6">
		{#if activeTab === 'overview'}
			<div class="grid gap-6 xl:grid-cols-12">
				<!-- 세계관 정보 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-4">
					<h2 class="mb-4 text-sm font-semibold">세계관 정보</h2>
					<div class="space-y-3">
						<div>
							<p class="mb-1 text-xs text-text-muted">이름</p>
							<p class="font-medium">{arcadiaWorld.name}</p>
						</div>
						<div class="flex flex-wrap gap-2">
							{#each arcadiaWorld.genre as g}
								<Badge label={g} variant="primary" />
							{/each}
						</div>
						<p class="text-sm text-text-secondary">{arcadiaWorld.oneLiner}</p>
						<p class="text-sm leading-relaxed text-text-muted">{arcadiaWorld.description}</p>
					</div>
					<div class="mt-4">
						<p class="mb-2 text-xs text-text-muted">세계관 이미지</p>
						<div class="grid grid-cols-4 gap-2">
							{#each arcadiaWorld.gallery as img}
								<img src={img} alt="" class="aspect-square rounded-lg border border-white/10 object-cover" />
							{/each}
							<button
								type="button"
								class="flex aspect-square items-center justify-center rounded-lg border border-dashed border-white/20 text-text-muted hover:border-primary-500 hover:text-primary-300"
							>
								<Plus class="h-5 w-5" />
							</button>
						</div>
					</div>
				</section>

				<!-- 지도 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-5">
					<div class="mb-4 flex items-center justify-between">
						<h2 class="text-sm font-semibold">아르카디아 대륙</h2>
						<Button variant="secondary" class="gap-2 text-xs">
							<Map class="h-3.5 w-3.5" /> 지도 편집
						</Button>
					</div>
					<div class="relative overflow-hidden rounded-xl border border-white/10 bg-bg-primary/60">
						<img
							src={arcadiaWorld.mapImage}
							alt="아르카디아 대륙 지도"
							class="aspect-[4/3] w-full object-cover opacity-80"
						/>
						<div class="absolute inset-0 flex flex-wrap items-center justify-center gap-3 p-4">
							{#each ['신성 제국', '엘프의 숲', '드워프 왕국', '자유 연합', '붉은 사막', '해상 무역 도시'] as region}
								<span class="rounded-full bg-bg-primary/80 px-3 py-1 text-[10px] backdrop-blur">
									{region}
								</span>
							{/each}
						</div>
					</div>
				</section>

				<!-- 주요 세력 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-3">
					<h2 class="mb-4 text-sm font-semibold">주요 세력</h2>
					<div class="space-y-3">
						{#each worldFactions as faction}
							<div class="flex items-start gap-3 rounded-xl border border-white/10 bg-bg-primary/40 p-3">
								<span class="text-xl">{faction.icon}</span>
								<div class="min-w-0 flex-1">
									<div class="flex items-center justify-between">
										<p class="text-sm font-medium">{faction.name}</p>
										<span class="text-xs text-primary-300">{faction.power}</span>
									</div>
									<p class="text-[10px] text-text-muted">{faction.alignment}</p>
									<p class="mt-1 text-xs text-text-secondary">{faction.description}</p>
								</div>
							</div>
						{/each}
					</div>
					<button type="button" class="mt-3 text-xs text-primary-400 hover:underline">
						전체 세력 보기 →
					</button>
				</section>

				<!-- 주요 테마 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-3">
					<h2 class="mb-4 text-sm font-semibold">주요 테마</h2>
					<div class="space-y-2">
						{#each worldThemes as theme}
							<div class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-primary/40 px-4 py-3">
								<span class="h-2 w-2 rounded-full" style="background: {theme.color}"></span>
								<span class="text-sm">{theme.title}</span>
							</div>
						{/each}
					</div>
					<Button variant="secondary" class="mt-4 w-full text-xs">테마 추가</Button>
				</section>

				<!-- 연대표 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-5">
					<div class="mb-4 flex items-center justify-between">
						<h2 class="text-sm font-semibold">연대표</h2>
						<Button variant="secondary" class="text-xs">연대표 편집</Button>
					</div>
					<div class="flex gap-2 overflow-x-auto pb-2">
						{#each worldEras as era, i}
							<div
								class="min-w-[100px] shrink-0 rounded-xl border border-white/10 bg-bg-primary/40 p-3 text-center {i ===
								worldEras.length - 1
									? 'ring-1 ring-primary-500/50'
									: ''}"
							>
								<p class="text-xs font-medium text-primary-300">{era.name}</p>
								<p class="text-[10px] text-text-muted">{era.range}</p>
								<p class="mt-1 text-[10px] text-text-secondary">{era.subtitle}</p>
							</div>
						{/each}
					</div>
				</section>

				<!-- 절대 법칙 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-4">
					<h2 class="mb-4 text-sm font-semibold">절대 법칙</h2>
					<div class="grid grid-cols-2 gap-3">
						{#each worldLaws as law}
							<div class="rounded-xl border border-white/10 bg-bg-primary/40 p-3">
								<span class="text-lg">{law.icon}</span>
								<p class="mt-1 text-xs font-medium">{law.title}</p>
								<p class="mt-1 text-[10px] leading-relaxed text-text-muted">{law.description}</p>
							</div>
						{/each}
						<button
							type="button"
							class="flex flex-col items-center justify-center rounded-xl border border-dashed border-white/20 p-3 text-text-muted hover:border-primary-500"
						>
							<Plus class="h-5 w-5" />
							<span class="mt-1 text-[10px]">법칙 추가</span>
						</button>
					</div>
				</section>

				<!-- 주요 사건 -->
				<section class="rounded-2xl border border-white/10 bg-bg-card/30 p-5 xl:col-span-12 lg:col-span-4">
					<h2 class="mb-4 text-sm font-semibold">주요 사건</h2>
					<div class="space-y-2">
						{#each worldEvents as event}
							<div class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-primary/40 px-4 py-3">
								<span class="w-14 shrink-0 text-xs text-text-muted">
									{event.year > 0 ? `AD ${event.year}` : `BC ${Math.abs(event.year)}`}
								</span>
								<p class="min-w-0 flex-1 truncate text-sm">{event.name}</p>
								<span
									class="shrink-0 rounded-md px-2 py-0.5 text-[10px]"
									style="background: {event.categoryColor}22; color: {event.categoryColor}"
								>
									{event.category}
								</span>
							</div>
						{/each}
					</div>
					<div class="mt-3 flex gap-3">
						<Button variant="secondary" class="text-xs">사건 추가</Button>
						<button type="button" class="text-xs text-primary-400 hover:underline">
							전체 사건 보기 →
						</button>
					</div>
				</section>
			</div>
		{:else if activeTab === 'faction'}
			<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
				{#each worldFactions as faction}
					<div class="rounded-2xl border border-white/10 bg-bg-card/30 p-5">
						<div class="mb-3 flex items-center gap-3">
							<span class="text-2xl">{faction.icon}</span>
							<div>
								<p class="font-semibold">{faction.name}</p>
								<p class="text-xs text-text-muted">{faction.alignment}</p>
							</div>
						</div>
						<p class="text-sm text-text-secondary">{faction.description}</p>
						<p class="mt-3 text-sm text-primary-300">세력치 {faction.power}</p>
					</div>
				{/each}
			</div>
		{:else if activeTab === 'timeline'}
			<div class="mx-auto max-w-3xl space-y-4">
				{#each worldEras as era}
					<div class="flex gap-4 rounded-2xl border border-white/10 bg-bg-card/30 p-5">
						<div class="w-24 shrink-0 text-right">
							<p class="text-sm font-medium text-primary-300">{era.name}</p>
							<p class="text-xs text-text-muted">{era.range}</p>
						</div>
						<div class="border-l border-white/10 pl-4">
							<p class="font-medium">{era.subtitle}</p>
							<p class="mt-1 text-sm text-text-muted">이 시대의 주요 사건과 인물을 기록합니다.</p>
						</div>
					</div>
				{/each}
			</div>
		{:else if activeTab === 'law'}
			<div class="grid gap-4 sm:grid-cols-2">
				{#each worldLaws as law}
					<div class="rounded-2xl border border-white/10 bg-bg-card/30 p-5">
						<span class="text-2xl">{law.icon}</span>
						<h3 class="mt-2 font-semibold">{law.title}</h3>
						<p class="mt-2 text-sm text-text-secondary">{law.description}</p>
					</div>
				{/each}
			</div>
		{:else if activeTab === 'event'}
			<div class="space-y-3">
				{#each worldEvents as event}
					<div class="flex items-center gap-4 rounded-2xl border border-white/10 bg-bg-card/30 px-5 py-4">
						<span class="w-20 text-sm text-text-muted">
							{event.year > 0 ? `AD ${event.year}` : `BC ${Math.abs(event.year)}`}
						</span>
						<p class="flex-1 font-medium">{event.name}</p>
						<Badge label={event.category} />
					</div>
				{/each}
			</div>
		{:else}
			<div class="flex min-h-[40vh] flex-col items-center justify-center text-center">
				<p class="text-lg font-semibold">{worldStudioTabs.find((t) => t.id === activeTab)?.label}</p>
				<p class="mt-2 max-w-md text-sm text-text-muted">
					{world.name} · Phase 2 편집기 — 상세 CRUD는 Phase 3에서 구현됩니다.
				</p>
				<Button variant="secondary" class="mt-6" href="/relationship">관계 편집기 열기</Button>
			</div>
		{/if}
	</div>
</div>
