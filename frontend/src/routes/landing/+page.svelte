<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import { Compass, Pencil, Sparkles, Globe } from 'lucide-svelte';
</script>

<svelte:head>
	<title>AI Character Playground — 랜딩</title>
</svelte:head>

<div class="relative min-h-screen overflow-hidden bg-bg-primary">
	<div class="absolute inset-0 bg-gradient-to-br from-primary-900/40 via-bg-primary to-bg-primary"></div>

	<header class="relative z-10 flex items-center justify-between px-8 py-5">
		<a href="/landing" class="flex items-center gap-2">
			<Sparkles class="h-5 w-5 text-primary-400" />
			<div class="leading-tight">
				<p class="text-sm font-semibold">AI Character</p>
				<p class="text-[10px] tracking-widest text-text-muted">PLAYGROUND</p>
			</div>
		</a>
		<div class="flex items-center gap-6 text-sm text-text-secondary">
			<button class="flex items-center gap-1 hover:text-text-primary">언어 ▾</button>
			<a href="/mobile" class="hover:text-text-primary">Mobile</a>
		</div>
	</header>

	<main class="relative z-10 mx-auto grid max-w-7xl items-center gap-12 px-8 py-8 lg:grid-cols-2 lg:py-16">
		<div class="overflow-hidden rounded-3xl border border-white/10 shadow-2xl">
			<img
				src="/images/landing-hero.png"
				alt="판타지 세계 일러스트"
				class="h-full w-full object-cover object-left"
			/>
		</div>

		<div class="flex flex-col items-start gap-6">
			<div>
				<h1 class="text-4xl font-bold leading-tight md:text-5xl">
					AI Character<br />
					<span class="gradient-text">Playground</span>
					<Sparkles class="ml-2 inline h-6 w-6 text-primary-400" />
				</h1>
				<p class="mt-4 text-xl text-text-primary">당신만의 세계를 살아보세요</p>
				<div class="mt-3 flex items-center gap-3 text-sm text-text-muted">
					<span class="h-px w-8 bg-white/20"></span>
					<span>✦ AI와 함께 만드는 무한한 이야기 ✦</span>
					<span class="h-px w-8 bg-white/20"></span>
				</div>
			</div>

			<div class="flex w-full max-w-sm flex-col gap-3">
				<Button href="/explore" size="lg" fullWidth>
					<Compass class="h-4 w-4" />
					캐릭터 탐험하기
				</Button>
				<Button variant="secondary" href="/studio/world" size="lg" fullWidth>
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
					{#each ['a', 'b', 'c', 'd'] as seed}
						<img
							src="https://api.dicebear.com/9.x/notionists/svg?seed={seed}"
							alt=""
							class="h-8 w-8 rounded-full border-2 border-bg-primary bg-bg-card"
						/>
					{/each}
				</div>
				<p class="text-sm text-primary-300">10,234명의 모험가가 함께하고 있어요</p>
			</div>
		</div>
	</main>

	<footer class="relative z-10 flex flex-col items-center justify-between gap-4 border-t border-white/10 px-8 py-6 text-xs text-text-muted md:flex-row">
		<p>© 2024 4-starspark. All rights reserved. · Powered by Living World Engine</p>
		<div class="flex items-center gap-4">
			<span class="hover:text-text-secondary">이용약관</span>
			<span class="hover:text-text-secondary">개인정보처리방침</span>
			<span class="hover:text-text-secondary">문의하기</span>
		</div>
	</footer>
</div>
