<script lang="ts">
	import { onMount } from 'svelte';
	import ScreenSearchBar from '$lib/components/mockup/ScreenSearchBar.svelte';
	import MockSectionHeader from '$lib/components/mockup/MockSectionHeader.svelte';
	import CharacterPortraitCard from '$lib/components/mockup/CharacterPortraitCard.svelte';
	import WorldStripCard from '$lib/components/mockup/WorldStripCard.svelte';
	import HomeDashboardPanel from '$lib/components/home/HomeDashboardPanel.svelte';
	import GuestHomePanel from '$lib/components/home/GuestHomePanel.svelte';
	import {
		getCatalogCharacters,
		getCatalogWorlds,
		getCatalogLoadError,
		getDailyQuests,
		isCatalogLoading
	} from '$lib/stores/catalog.svelte';
	import { initEmotionApi } from '$lib/stores/emotion.svelte';
	import { initRelationship } from '$lib/stores/relationship.svelte';
	import { isLoggedIn } from '$lib/stores/auth.svelte';
	import { Target } from 'lucide-svelte';

	const characters = $derived(getCatalogCharacters());
	const worlds = $derived(getCatalogWorlds());
	const dailyQuests = $derived(getDailyQuests());
	const loading = $derived(isCatalogLoading());
	const loadError = $derived(getCatalogLoadError());
	const loggedIn = $derived(isLoggedIn());

	const heroCharacter = $derived(characters[0]);
	const recommendedCharacters = $derived(characters.slice(0, 6));
	const popularWorlds = $derived(worlds.slice(0, 5));

	const questCards = $derived([
		...dailyQuests,
		{
			id: 'q4',
			title: '관계도 1회 탐색',
			progress: 0,
			total: 1,
			reward: 'XP +15'
		}
	].slice(0, 4));

	onMount(() => {
		if (!isLoggedIn()) return;
		void initRelationship({ world: 'arcadia', center: 'elia' });
		void initEmotionApi('elia');
	});
</script>

<svelte:head>
	<title>홈 — ACP</title>
</svelte:head>

<div class="-m-2 min-h-full bg-mock-bg p-2 lg:-m-4 lg:p-4">
	<ScreenSearchBar placeholder="캐릭터, 세계관, 스토리 검색…" />

	{#if loadError}
		<div class="mb-4 rounded-xl border border-accent-red/30 bg-accent-red/10 px-4 py-3 text-sm text-accent-red">
			{loadError}
		</div>
	{/if}

	<div class="flex gap-5">
		<div class="min-w-0 flex-1 space-y-6">
			<!-- 히어로 배너 -->
			<section class="relative overflow-hidden rounded-xl border border-mock-border">
				<div class="absolute inset-0 bg-gradient-to-r from-mock-bg via-mock-bg/70 to-transparent"></div>
				{#if heroCharacter}
					<img
						src={heroCharacter.cover}
						alt=""
						class="absolute inset-0 h-full w-full object-cover opacity-40"
					/>
				{/if}
				<div class="relative flex min-h-[200px] flex-col justify-center gap-3 p-8 md:max-w-lg">
					<p class="text-[10px] font-medium tracking-[0.2em] text-mock-accent">LIVING WORLD ENGINE</p>
					<h2 class="text-2xl leading-snug font-bold md:text-3xl">
						당신만의 캐릭터와<br />특별한 이야기를 만들어가세요
					</h2>
					<p class="text-sm text-text-secondary">오늘도 새로운 이야기가 시작됩니다</p>
					<a
						href="/explore"
						class="mt-1 inline-flex w-fit items-center gap-2 rounded-lg bg-mock-accent px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-mock-accent/90"
					>
						캐릭터 탐험하기 →
					</a>
				</div>
			</section>

			{#if loading}
				<p class="text-center text-sm text-text-muted">데이터를 불러오는 중…</p>
			{/if}

			<!-- 추천 캐릭터 -->
			<section>
				<MockSectionHeader title="추천 캐릭터" href="/explore" />
				<div class="flex gap-3 overflow-x-auto pb-1">
					{#each recommendedCharacters as character}
						<CharacterPortraitCard {character} />
					{:else}
						<p class="text-sm text-text-muted">등록된 캐릭터가 없습니다.</p>
					{/each}
				</div>
			</section>

			<!-- 인기 세계관 -->
			<section>
				<MockSectionHeader title="인기 세계관" href="/explore" />
				<div class="flex gap-3 overflow-x-auto pb-1">
					{#each popularWorlds as world}
						<WorldStripCard {world} />
					{/each}
				</div>
			</section>

			<!-- 오늘의 추천 콘텐츠 -->
			{#if loggedIn}
				<section>
					<MockSectionHeader title="오늘의 추천 콘텐츠" />
					<div class="grid grid-cols-2 gap-3 lg:grid-cols-4">
						{#each questCards as quest}
							<div class="rounded-xl border border-mock-border bg-mock-panel p-4 transition hover:border-mock-accent/30">
								<div class="mb-2 flex items-start justify-between gap-2">
									<p class="text-sm font-medium leading-snug">{quest.title}</p>
									<span class="shrink-0 rounded-md bg-mock-accent/15 px-2 py-0.5 text-[10px] text-mock-accent">
										{quest.reward}
									</span>
								</div>
								<div class="h-1.5 overflow-hidden rounded-full bg-mock-track">
									<div
										class="h-full rounded-full bg-mock-accent transition-all"
										style="width: {(quest.progress / quest.total) * 100}%"
									></div>
								</div>
								<p class="mt-1.5 flex items-center gap-1 text-[10px] text-text-muted">
									<Target class="h-3 w-3" />
									{quest.progress >= quest.total ? '완료' : `${quest.progress}/${quest.total}`}
								</p>
							</div>
						{/each}
					</div>
				</section>
			{/if}
		</div>

		<div class="hidden shrink-0 xl:block">
			{#if loggedIn}
				<HomeDashboardPanel />
			{:else}
				<GuestHomePanel />
			{/if}
		</div>
	</div>
</div>
