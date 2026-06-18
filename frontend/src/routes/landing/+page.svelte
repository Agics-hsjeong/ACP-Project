<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import CharacterCard from '$lib/components/cards/CharacterCard.svelte';
	import { getCatalogCharacters } from '$lib/stores/catalog.svelte';
	import { getLandingFeatures } from '$lib/stores/content.svelte';
	import { getLoginUrl } from '$lib/auth/access';
	import { Compass, Pencil, Sparkles, Globe, Brain, Heart, Users } from 'lucide-svelte';

	const characters = $derived(getCatalogCharacters());
	const popular = $derived(characters.slice(0, 4));
	const landingFeatures = $derived(getLandingFeatures());
	const heroImage =
		'https://api.dicebear.com/9.x/shapes/svg?seed=landing-hero&backgroundColor=312e81&scale=90';
</script>

<svelte:head>
	<title>AI Character Playground — 랜딩</title>
</svelte:head>

<div class="relative min-h-screen overflow-hidden bg-bg-primary">
	<div class="absolute inset-0 bg-gradient-to-br from-primary-900/40 via-bg-primary to-bg-primary"></div>

	<header class="relative z-10 flex items-center justify-between px-8 py-5">
		<a href="/landing" class="flex items-center gap-2">
			<img src="/logo.svg" alt="ACP 로고" class="h-10 w-10 rounded-lg bg-white/5 object-contain" />
			<div class="leading-tight">
				<p class="text-sm font-semibold">AI Character</p>
				<p class="text-[10px] tracking-widest text-text-muted">PLAYGROUND</p>
			</div>
		</a>
		<div class="flex items-center gap-6 text-sm text-text-secondary">
			<a href="/login" class="hover:text-text-primary">로그인</a>
			<a href="/mobile" class="hover:text-text-primary">Mobile</a>
		</div>
	</header>

	<main class="relative z-10 mx-auto max-w-7xl px-8 py-8">
		<section class="grid items-center gap-12 lg:grid-cols-2 lg:py-8">
			<div class="overflow-hidden rounded-3xl border border-white/10 shadow-2xl">
				<img src={heroImage} alt="판타지 세계 일러스트" class="aspect-[4/3] w-full object-cover" />
			</div>

			<div class="flex flex-col items-start gap-6">
				<div>
					<h1 class="text-4xl font-bold leading-tight md:text-5xl">
						AI Character<br />
						<span class="gradient-text">Playground</span>
						<Sparkles class="ml-2 inline h-6 w-6 text-primary-400" />
					</h1>
					<p class="mt-4 text-xl text-text-primary">당신만의 세계를 살아보세요</p>
					<p class="mt-2 text-sm text-text-muted">Living World Engine · Memory · Emotion · Relationship</p>
				</div>

				<div class="flex w-full max-w-sm flex-col gap-3">
					<Button href="/explore" size="lg" fullWidth>
						<Compass class="h-4 w-4" />
						캐릭터 탐험하기
					</Button>
					<Button variant="secondary" href={getLoginUrl('/studio/world')} size="lg" fullWidth>
						<Pencil class="h-4 w-4" />
						나만의 세계관 만들기
					</Button>
					<Button variant="secondary" href="/explore" size="lg" fullWidth>
						<Globe class="h-4 w-4" />
						인기 세계관 둘러보기
					</Button>
				</div>

				<div class="flex items-center gap-3">
					<div class="flex -space-x-2">
						{#each popular as c}
							<img src={c.avatar} alt="" class="h-8 w-8 rounded-full border-2 border-bg-primary bg-bg-card" />
						{/each}
					</div>
					<p class="text-sm text-primary-300">10,234명의 모험가가 함께하고 있어요</p>
				</div>
			</div>
		</section>

		<section class="mt-16 border-t border-white/10 pt-16">
			<div class="mb-8 flex items-center gap-2">
				<Users class="h-5 w-5 text-primary-400" />
				<h2 class="text-2xl font-bold">인기 캐릭터</h2>
			</div>
			<div class="flex gap-4 overflow-x-auto pb-4">
				{#each popular as character}
					<CharacterCard {character} />
				{/each}
			</div>
		</section>

		<section class="mt-16 border-t border-white/10 pt-16">
			<h2 class="mb-8 text-2xl font-bold">서비스 소개</h2>
			<div class="grid gap-6 md:grid-cols-3">
				{#each landingFeatures as feature, i}
					<div class="rounded-2xl border border-white/10 bg-bg-surface/40 p-6">
						{#if i === 0}
							<Brain class="mb-3 h-8 w-8 text-primary-400" />
						{:else if i === 1}
							<Heart class="mb-3 h-8 w-8 text-accent-pink" />
						{:else}
							<Globe class="mb-3 h-8 w-8 text-accent-green" />
						{/if}
						<h3 class="font-semibold">{feature.title}</h3>
						<p class="mt-2 text-sm text-text-secondary">{feature.description}</p>
					</div>
				{/each}
			</div>
		</section>
	</main>

	<footer class="relative z-10 mt-16 flex flex-col items-center justify-between gap-4 border-t border-white/10 px-8 py-6 text-xs text-text-muted md:flex-row">
		<p>© 2024 4-starspark. All rights reserved. · Powered by Living World Engine</p>
		<div class="flex items-center gap-4">
			<span class="hover:text-text-secondary">이용약관</span>
			<span class="hover:text-text-secondary">개인정보처리방침</span>
			<span class="hover:text-text-secondary">문의하기</span>
		</div>
	</footer>
</div>
