<script lang="ts">
	import { page } from '$app/stores';
	import { getCharacter, worlds } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { Heart, Share2, MessageCircle, Quote } from 'lucide-svelte';

	const character = $derived(getCharacter($page.params.id) ?? getCharacter('elia')!);
	const world = $derived(worlds.find((w) => w.id === character.worldId || w.name === character.world));
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
				<button class="rounded-xl border border-white/10 p-3 hover:bg-white/5" aria-label="즐겨찾기">
					<Heart class="h-5 w-5" />
				</button>
				<button class="rounded-xl border border-white/10 p-3 hover:bg-white/5" aria-label="공유">
					<Share2 class="h-5 w-5" />
				</button>
			</div>

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
		</div>
	</div>
</div>
