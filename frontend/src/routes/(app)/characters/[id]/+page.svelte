<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import MockPanel from '$lib/components/mockup/MockPanel.svelte';
	import EmotionRadar from '$lib/components/emotion/EmotionRadar.svelte';
	import { getCatalogCharacter, getCatalogWorlds, getCatalogMemoryStats } from '$lib/stores/catalog.svelte';
	import { initScenarios, getCharacterScenarios } from '$lib/stores/scenarios.svelte';
	import { initRelationship, getEliaRelationships } from '$lib/stores/relationship.svelte';
	import { initEmotionApi, getEmotions, getIntimacy } from '$lib/stores/emotion.svelte';
	import { isFavorite, toggleFavorite } from '$lib/stores/favorites.svelte';
	import { isLoggedIn, redirectToLogin } from '$lib/stores/auth.svelte';
	import type { EmotionAxis } from '$lib/data/mock';
	import { ArrowLeft, Heart, Share2, MessageCircle, Eye, Quote } from 'lucide-svelte';

	const characterId = $derived($page.params.id ?? '');
	const character = $derived(getCatalogCharacter(characterId));
	const worlds = $derived(getCatalogWorlds());
	const world = $derived(
		worlds.find((w) => w.id === character?.worldId || w.name === character?.world)
	);
	const scenarios = $derived(character ? getCharacterScenarios(character.id) : []);
	const eliaRelationships = $derived(getEliaRelationships());
	const emotions = $derived(getEmotions());
	const intimacy = $derived(getIntimacy());
	const memoryStats = $derived(getCatalogMemoryStats());
	const loggedIn = $derived(isLoggedIn());

	let activeTab = $state<'profile' | 'story' | 'memory' | 'relation' | 'lines'>('profile');
	let selectedImage = $state(0);
	let favorited = $derived(character ? isFavorite(character.id) : false);
	let shareToast = $state(false);

	const mockEmotionColors: Record<string, string> = {
		affection: 'var(--color-emo-affection)',
		trust: 'var(--color-emo-trust)',
		respect: 'var(--color-emo-respect)',
		anger: 'var(--color-emo-anger)',
		jealousy: 'var(--color-emo-jealousy)',
		fear: 'var(--color-emo-fear)'
	};

	const displayEmotions = $derived(
		emotions.map((e) => ({
			...e,
			color: mockEmotionColors[e.key] ?? e.color
		})) as EmotionAxis[]
	);

	const studioMeta = $derived((character?.studioMeta ?? {}) as Record<string, unknown>);
	const affiliation = $derived(String(studioMeta.affiliation ?? character?.world ?? '—'));
	const position = $derived(String(studioMeta.position ?? character?.occupation ?? '—'));
	const mbti = $derived(String(studioMeta.mbti ?? '—'));
	const personalityText = $derived(character?.personality.join(', ') ?? '—');

	const gallery = $derived.by(() => {
		if (!character) return [] as string[];
		const fromMeta = (studioMeta.gallery as string[] | undefined) ?? [];
		const base = [character.avatar, character.cover, ...fromMeta].filter(Boolean);
		return [...new Set(base)];
	});

	const relationships = $derived(
		character?.id === 'elia'
			? eliaRelationships
			: eliaRelationships.filter((r) => r.characterId === character?.id)
	);

	const tabs = [
		{ id: 'profile' as const, label: '프로필' },
		{ id: 'story' as const, label: '스토리' },
		{ id: 'memory' as const, label: '기억' },
		{ id: 'relation' as const, label: '관계' },
		{ id: 'lines' as const, label: '대사' }
	];

	$effect(() => {
		if (gallery.length) selectedImage = Math.min(selectedImage, gallery.length - 1);
	});

	onMount(() => {
		if (!character) return;
		if (isLoggedIn()) {
			void initScenarios(character.id);
			void initRelationship({ center: character.id === 'elia' ? 'elia' : 'elia' });
			void initEmotionApi(character.id);
		}
	});

	function handleFavorite() {
		if (!character) return;
		if (!loggedIn) {
			redirectToLogin(`/characters/${character.id}`);
			return;
		}
		toggleFavorite(character.id);
	}

	function startChat(scenarioId?: string) {
		if (!character) return;
		const path = scenarioId
			? `/chat/${character.id}?scenario=${scenarioId}`
			: `/chat/${character.id}`;
		if (!loggedIn) {
			redirectToLogin(path);
			return;
		}
		goto(path);
	}

	function handleShare() {
		if (!character) return;
		if (navigator.share) {
			navigator.share({ title: character.name, url: window.location.href });
		} else {
			navigator.clipboard?.writeText(window.location.href);
			shareToast = true;
			setTimeout(() => (shareToast = false), 2000);
		}
	}
</script>

<svelte:head>
	<title>{character?.name ?? '캐릭터'} — 캐릭터 상세</title>
</svelte:head>

{#if !character}
	<div class="mx-auto max-w-lg rounded-xl border border-mock-border bg-mock-panel p-8 text-center">
		<h1 class="text-xl font-bold">캐릭터를 찾을 수 없습니다</h1>
		<p class="mt-2 text-sm text-text-muted">요청한 캐릭터가 존재하지 않거나 삭제되었습니다.</p>
		<a href="/explore" class="mt-4 inline-block text-sm text-mock-accent hover:underline">탐색으로 돌아가기</a>
	</div>
{:else}
<div class="-m-2 min-h-full bg-mock-bg p-2 lg:-m-4 lg:p-4">
	<a
		href="/explore"
		class="mb-4 inline-flex items-center gap-1.5 text-sm text-text-muted transition hover:text-mock-accent"
	>
		<ArrowLeft class="h-4 w-4" />
		캐릭터 탐색으로
	</a>

	{#if !loggedIn}
		<div class="mb-4 rounded-xl border border-mock-accent/20 bg-mock-accent/5 px-4 py-3 text-sm text-text-secondary">
			둘러보기 모드입니다. 대화·시나리오·관계 정보는
			<button
				type="button"
				class="font-medium text-mock-accent underline hover:text-mock-accent/80"
				onclick={() => redirectToLogin(`/characters/${character.id}`)}
			>
				로그인
			</button>
			후 이용할 수 있습니다.
		</div>
	{/if}

	<div class="flex flex-col gap-5 xl:flex-row">
		<!-- 초상화 열 -->
		<div class="w-full shrink-0 xl:w-[270px]">
			<MockPanel padding={false} class="overflow-hidden">
				<img
					src={gallery[selectedImage] ?? character.avatar}
					alt={character.name}
					class="aspect-[3/4] w-full object-cover"
				/>
			</MockPanel>
			{#if gallery.length > 1}
				<div class="mt-2 flex gap-2 overflow-x-auto pb-1">
					{#each gallery as img, i}
						<button
							type="button"
							class="h-14 w-14 shrink-0 overflow-hidden rounded-lg border-2 transition {selectedImage === i
								? 'border-mock-accent'
								: 'border-mock-border opacity-70 hover:opacity-100'}"
							onclick={() => (selectedImage = i)}
						>
							<img src={img} alt="" class="h-full w-full object-cover" />
						</button>
					{/each}
				</div>
			{/if}
			<div class="mt-3 flex gap-2">
				<button
					type="button"
					class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-mock-accent py-2.5 text-sm font-semibold text-white transition hover:bg-mock-accent/90"
					onclick={() => startChat()}
				>
					<MessageCircle class="h-4 w-4" />
					{loggedIn ? '대화 시작' : '로그인 후 대화'}
				</button>
				<button
					type="button"
					class="rounded-xl border border-mock-border p-2.5 transition hover:border-mock-accent/40 {favorited
						? 'text-emo-affection'
						: 'text-text-muted'}"
					aria-label="즐겨찾기"
					onclick={handleFavorite}
				>
					<Heart class="h-5 w-5" fill={favorited ? 'currentColor' : 'none'} />
				</button>
				<button
					type="button"
					class="rounded-xl border border-mock-border p-2.5 text-text-muted transition hover:border-mock-accent/40"
					aria-label="공유"
					onclick={handleShare}
				>
					<Share2 class="h-5 w-5" />
				</button>
			</div>
			{#if shareToast}
				<p class="mt-1 text-center text-xs text-emo-respect">링크가 복사되었습니다</p>
			{/if}
		</div>

		<!-- 정보 패널 -->
		<div class="min-w-0 flex-1 space-y-5">
			<div>
				<span class="inline-block rounded-md border border-mock-accent/30 bg-mock-accent/10 px-2.5 py-0.5 text-xs text-mock-accent">
					{character.world}
				</span>
				<h1 class="mt-2 text-3xl font-bold">{character.name}</h1>
				<p class="mt-0.5 text-base text-text-secondary">{character.title}</p>
				<div class="mt-2 flex items-center gap-4 text-sm text-text-muted">
					<span class="flex items-center gap-1 text-emo-affection">
						<Heart class="h-3.5 w-3.5" />
						{character.likes}%
					</span>
					<span class="flex items-center gap-1">
						<Eye class="h-3.5 w-3.5" />
						{(character.views / 1000).toFixed(1)}k 조회
					</span>
				</div>
			</div>

			{#if character.quote}
				<blockquote class="flex gap-3 rounded-xl border border-mock-border bg-mock-panel p-4 text-sm italic text-text-secondary">
					<Quote class="h-5 w-5 shrink-0 text-mock-accent" />
					{character.quote}
				</blockquote>
			{/if}

			<p class="text-xs text-text-muted">
				{character.race}{character.age ? ` · ${character.age}세` : ''} · {character.gender ?? '—'}
			</p>

			<!-- 탭 -->
			<div class="flex gap-1 overflow-x-auto border-b border-mock-border pb-px">
				{#each tabs as tab}
					<button
						type="button"
						class="shrink-0 border-b-2 px-4 py-2 text-sm transition {activeTab === tab.id
							? 'border-mock-accent font-semibold text-mock-accent'
							: 'border-transparent text-text-muted hover:text-text-secondary'}"
						onclick={() => (activeTab = tab.id)}
					>
						{tab.label}
					</button>
				{/each}
			</div>

			{#if activeTab === 'profile'}
				<MockPanel>
					<div class="grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-4">
						<div>
							<p class="text-[11px] text-text-muted">소속</p>
							<p class="mt-1 text-sm font-medium">{affiliation}</p>
						</div>
						<div>
							<p class="text-[11px] text-text-muted">직위</p>
							<p class="mt-1 text-sm font-medium">{position}</p>
						</div>
						<div>
							<p class="text-[11px] text-text-muted">성격</p>
							<p class="mt-1 text-sm font-medium">{personalityText}</p>
						</div>
						<div>
							<p class="text-[11px] text-text-muted">MBTI</p>
							<p class="mt-1 text-sm font-medium">{mbti}</p>
						</div>
					</div>
					<div class="mt-5 border-t border-mock-border pt-4">
						<h3 class="mb-2 text-sm font-semibold">소개</h3>
						<p class="text-sm leading-relaxed text-text-secondary">{character.description}</p>
					</div>
				</MockPanel>
			{:else if activeTab === 'story'}
				<MockPanel>
					<p class="text-sm leading-relaxed text-text-secondary">
						{character.memorySummary ?? character.description}
					</p>
					{#if loggedIn && scenarios.length}
						<div class="mt-4 space-y-2">
							<p class="text-xs font-medium text-text-muted">시나리오</p>
							{#each scenarios as scenario}
								<button
									type="button"
									class="w-full rounded-lg border border-mock-border bg-mock-bg/40 px-3 py-2 text-left text-sm transition hover:border-mock-accent/40"
									onclick={() => startChat(scenario.scenario_id)}
								>
									<p class="font-medium">{scenario.title}</p>
									<p class="text-xs text-text-muted">{scenario.description}</p>
								</button>
							{/each}
						</div>
					{/if}
				</MockPanel>
			{:else if activeTab === 'memory'}
				<MockPanel>
					<p class="text-sm text-text-secondary">
						{character.memorySummary ??
							'아직 저장된 기억이 없습니다. 대화를 시작하면 에피소드가 자동으로 기록됩니다.'}
					</p>
				</MockPanel>
			{:else if activeTab === 'relation'}
				<MockPanel>
					{#if relationships.length}
						<div class="space-y-2">
							{#each relationships.slice(0, 6) as rel}
								<div class="flex items-center justify-between rounded-lg border border-mock-border bg-mock-bg/40 px-3 py-2 text-sm">
									<span>{rel.name}</span>
									<div class="flex items-center gap-2">
										<div class="h-1.5 w-20 overflow-hidden rounded-full bg-mock-track">
											<div
												class="h-full rounded-full bg-mock-accent"
												style="width: {rel.score}%"
											></div>
										</div>
										<span class="text-xs text-text-muted">{rel.score}</span>
									</div>
								</div>
							{/each}
						</div>
						<a href="/relationship" class="mt-3 inline-block text-sm text-mock-accent hover:underline">
							전체 관계도 보기 →
						</a>
					{:else}
						<p class="text-sm text-text-muted">관계 데이터가 없습니다.</p>
					{/if}
				</MockPanel>
			{:else}
				<MockPanel>
					<p class="text-sm italic text-text-secondary">
						"{character.quote ?? `${character.name}의 대표 대사가 여기에 표시됩니다.`}"
					</p>
				</MockPanel>
			{/if}

			<!-- 갤러리 -->
			<section>
				<h2 class="mb-3 text-base font-bold">갤러리</h2>
				<div class="grid grid-cols-3 gap-2 sm:grid-cols-4">
					{#each gallery as img}
						<div class="aspect-square overflow-hidden rounded-lg border border-mock-border bg-mock-panel">
							<img src={img} alt="" class="h-full w-full object-cover" />
						</div>
					{/each}
				</div>
			</section>
		</div>

		<!-- 감정 패널 -->
		<div class="w-full shrink-0 xl:w-[380px]">
			<MockPanel title="감정 분석" class="mb-4">
				{#if displayEmotions.length}
					<EmotionRadar emotions={displayEmotions} size={200} />
					<div class="mt-4 space-y-2.5">
						{#each displayEmotions as emo}
							<div>
								<div class="mb-1 flex justify-between text-xs">
									<span>{emo.label}</span>
									<span class="text-text-muted">{emo.value}%</span>
								</div>
								<div class="h-1.5 rounded-full bg-mock-track">
									<div
										class="h-full rounded-full"
										style="width: {emo.value}%; background: {emo.color}"
									></div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="py-6 text-center text-xs text-text-muted">감정 데이터를 불러오는 중…</p>
				{/if}
			</MockPanel>

			<MockPanel title="관계 요약" class="mb-4">
				{#if relationships.length}
					<div class="space-y-2">
						{#each relationships.slice(0, 4) as rel}
							<div>
								<div class="mb-1 flex justify-between text-xs">
									<span>{rel.name}</span>
									<span class="text-text-muted">{rel.score}</span>
								</div>
								<div class="h-1.5 rounded-full bg-mock-track">
									<div
										class="h-full rounded-full bg-emo-trust"
										style="width: {rel.score}%"
									></div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-xs text-text-muted">관계 데이터가 없습니다.</p>
				{/if}
			</MockPanel>

			<MockPanel>
				<div class="flex items-center justify-between">
					<span class="text-sm text-text-muted">함께한 기간</span>
					<span class="text-2xl font-bold text-mock-accent">{memoryStats.daysTogether}일</span>
				</div>
				<div class="mt-3 flex items-center justify-between border-t border-mock-border pt-3">
					<span class="text-sm text-text-muted">친밀도</span>
					<span class="text-lg font-semibold text-emo-affection">{intimacy}%</span>
				</div>
			</MockPanel>
		</div>
	</div>
</div>
{/if}
