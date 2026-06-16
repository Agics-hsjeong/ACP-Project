<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { getCatalogCharacter, getCatalogWorlds } from '$lib/stores/catalog.svelte';
	import { initScenarios, getCharacterScenarios } from '$lib/stores/scenarios.svelte';
	import { initRelationship } from '$lib/stores/relationship.svelte';
	import { getEliaRelationships } from '$lib/stores/relationship.svelte';
	import { isFavorite, toggleFavorite } from '$lib/stores/favorites.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { Heart, Share2, MessageCircle, Quote, GitBranch } from 'lucide-svelte';

	const character = $derived(
		getCatalogCharacter($page.params.id ?? 'elia') ?? getCatalogCharacter('elia')!
	);
	const worlds = $derived(getCatalogWorlds());
	const world = $derived(worlds.find((w) => w.id === character.worldId || w.name === character.world));
	const scenarios = $derived(getCharacterScenarios(character.id));
	const eliaRelationships = $derived(getEliaRelationships());
	let selectedScenario = $state('default');
	let favorited = $derived(isFavorite(character.id));
	let shareToast = $state(false);

	onMount(() => {
		void initScenarios(character.id);
		void initRelationship({ center: 'elia' });
	});

	function handleFavorite() {
		toggleFavorite(character.id);
	}

	function handleShare() {
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
	<title>{character.name} — 캐릭터 상세</title>
</svelte:head>

<div class="mx-auto max-w-6xl">
	<div class="grid gap-8 lg:grid-cols-[340px_1fr]">
		<div class="space-y-4">
			<div class="overflow-hidden rounded-2xl border border-white/10 bg-bg-surface shadow-lg">
				<img src={character.avatar} alt={character.name} class="aspect-square w-full object-cover" />
			</div>
			<div class="flex gap-2">
				<Button href="/chat/{character.id}" fullWidth>
					<MessageCircle class="h-4 w-4" />
					대화 시작
				</Button>
				<button
					type="button"
					class="rounded-xl border border-white/10 p-3 hover:bg-white/5 {favorited
						? 'text-accent-pink'
						: ''}"
					aria-label="즐겨찾기"
					onclick={handleFavorite}
				>
					<Heart class="h-5 w-5" fill={favorited ? 'currentColor' : 'none'} />
				</button>
				<button
					type="button"
					class="rounded-xl border border-white/10 p-3 hover:bg-white/5"
					aria-label="공유"
					onclick={handleShare}
				>
					<Share2 class="h-5 w-5" />
				</button>
			</div>
			{#if shareToast}
				<p class="text-center text-xs text-accent-green">링크가 복사되었습니다</p>
			{/if}

			{#if scenarios.length}
				<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-4">
					<p class="mb-2 text-xs font-medium text-text-muted">시나리오 선택</p>
					<div class="space-y-2">
						{#each scenarios as scenario}
							<button
								type="button"
								onclick={() => {
									selectedScenario = scenario.id;
									goto(`/chat/${character.id}?scenario=${scenario.id}`);
								}}
								class="w-full rounded-xl border px-3 py-2 text-left text-sm transition {selectedScenario ===
								scenario.id
									? 'border-primary-500 bg-primary-600/20'
									: 'border-white/10 hover:bg-white/5'}"
							>
								<p class="font-medium">{scenario.title}</p>
								<p class="text-xs text-text-muted">{scenario.description}</p>
							</button>
						{/each}
					</div>
				</div>
			{/if}

			{#if world}
				<div class="rounded-2xl border border-white/10 bg-bg-surface/50 p-4">
					<p class="text-xs text-text-muted">소속 세계관</p>
					<p class="mt-1 font-semibold">{world.name}</p>
					<div class="mt-2 flex flex-wrap gap-1">
						{#each world.genre as g}
							<Badge label={g} variant="primary" />
						{/each}
					</div>
					<p class="mt-2 text-xs text-text-muted">{world.characterCount}명의 캐릭터</p>
				</div>
			{/if}
		</div>

		<div class="space-y-6">
			<div>
				<p class="text-sm text-primary-400">{character.world}</p>
				<h1 class="mt-1 text-3xl font-bold">{character.name}</h1>
				<p class="mt-1 text-lg text-text-secondary">{character.title}</p>
				<div class="mt-3 flex flex-wrap gap-2">
					{#each character.tags as tag}
						<Badge label={tag} variant="primary" />
					{/each}
				</div>
			</div>

			{#if character.quote}
				<blockquote
					class="flex gap-3 rounded-2xl border border-primary-500/20 bg-primary-500/10 p-5 text-sm italic text-primary-100"
				>
					<Quote class="h-5 w-5 shrink-0 text-primary-400" />
					{character.quote}
				</blockquote>
			{/if}

			<div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
				{#each [
					{ label: '나이', value: character.age ? `${character.age}세` : '—' },
					{ label: '직업', value: character.occupation },
					{ label: '종족', value: character.race },
					{ label: '호감도', value: `${character.likes}%` }
				] as stat}
					<div class="rounded-xl bg-bg-surface/60 p-4">
						<p class="text-xs text-text-muted">{stat.label}</p>
						<p class="mt-1 font-semibold">{stat.value}</p>
					</div>
				{/each}
			</div>

			<section>
				<h2 class="mb-2 font-semibold">소개</h2>
				<p class="text-sm leading-relaxed text-text-secondary">{character.description}</p>
			</section>

			<section>
				<h2 class="mb-2 font-semibold">성격</h2>
				<div class="flex flex-wrap gap-2">
					{#each character.personality as trait}
						<Badge label={trait} />
					{/each}
				</div>
			</section>

			<section>
				<h2 class="mb-2 font-semibold">기억 요약</h2>
				<div class="rounded-xl border border-white/10 bg-bg-surface/40 p-4 text-sm text-text-secondary">
					{character.memorySummary ??
						'아직 저장된 기억이 없습니다. 대화를 시작하면 에피소드가 자동으로 기록됩니다.'}
				</div>
			</section>

			{#if character.id === 'elia'}
				<section>
					<h2 class="mb-3 flex items-center gap-2 font-semibold">
						<GitBranch class="h-4 w-4 text-primary-400" />
						관계 요약
					</h2>
					<div class="grid gap-2 sm:grid-cols-2">
						{#each eliaRelationships.slice(0, 4) as rel}
							<div class="rounded-xl border border-white/10 bg-bg-surface/40 px-4 py-3 text-sm">
								<span class="text-text-muted">{rel.name}</span>
								<span class="ml-2 text-primary-300">{rel.score}</span>
							</div>
						{/each}
					</div>
					<a href="/relationship" class="mt-2 inline-block text-sm text-primary-400 hover:underline">
						전체 관계도 보기 →
					</a>
				</section>
			{/if}
		</div>
	</div>
</div>
