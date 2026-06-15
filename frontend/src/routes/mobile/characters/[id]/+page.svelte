<script lang="ts">
	import { page } from '$app/stores';
	import { getCharacter } from '$lib/data/mock';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { Heart, MessageCircle } from 'lucide-svelte';

	const character = $derived(getCharacter($page.params.id) ?? getCharacter('elia')!);
</script>

<svelte:head>
	<title>{character.name} — Mobile Profile</title>
</svelte:head>

<div class="relative">
	<img src={character.avatar} alt="" class="h-56 w-full object-cover" />
	<div class="absolute inset-0 bg-gradient-to-t from-bg-primary to-transparent"></div>
	<div class="absolute bottom-4 left-4 right-4">
		<p class="text-2xl font-bold">{character.name}</p>
		<p class="text-sm text-text-secondary">{character.title}</p>
		<p class="mt-1 text-xs text-accent-pink">호감도 {character.likes}%</p>
	</div>
</div>

<div class="space-y-4 p-4">
	<div class="grid grid-cols-3 gap-2 text-center text-xs">
		<div class="rounded-lg bg-bg-surface/60 p-2">
			<p class="text-text-muted">나이</p>
			<p class="font-semibold">{character.age ?? '—'}세</p>
		</div>
		<div class="rounded-lg bg-bg-surface/60 p-2">
			<p class="text-text-muted">직업</p>
			<p class="font-semibold">{character.occupation}</p>
		</div>
		<div class="rounded-lg bg-bg-surface/60 p-2">
			<p class="text-text-muted">종족</p>
			<p class="font-semibold">{character.race}</p>
		</div>
	</div>

	<p class="text-sm leading-relaxed text-text-secondary">{character.description}</p>

	{#if character.quote}
		<blockquote class="rounded-xl border border-primary-500/20 bg-primary-500/10 p-3 text-sm italic">
			{character.quote}
		</blockquote>
	{/if}

	<div class="flex flex-wrap gap-1">
		{#each character.tags as tag}
			<Badge label={tag} variant="primary" />
		{/each}
	</div>

	<div class="flex gap-2">
		<Button href="/mobile/chat/{character.id}" fullWidth>
			<MessageCircle class="h-4 w-4" />
			대화 시작
		</Button>
		<button class="rounded-xl border border-white/10 p-3" aria-label="즐겨찾기">
			<Heart class="h-5 w-5" />
		</button>
	</div>
</div>
