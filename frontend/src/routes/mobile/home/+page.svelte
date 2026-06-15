<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import { characters, recentChats } from '$lib/data/mock';
	import { MessageCircle, Sparkles } from 'lucide-svelte';

	const featured = characters[0];
</script>

<svelte:head>
	<title>홈 — Mobile</title>
</svelte:head>

<header class="flex items-center gap-2 border-b border-white/10 px-4 py-3">
	<Sparkles class="h-4 w-4 text-primary-400" />
	<span class="text-sm font-semibold">AI Character Playground</span>
</header>

<section class="relative m-4 overflow-hidden rounded-2xl border border-white/10">
	<img src={featured.cover} alt="" class="h-40 w-full object-cover opacity-60" />
	<div class="absolute inset-0 bg-gradient-to-t from-bg-primary via-transparent to-transparent"></div>
	<div class="absolute bottom-0 p-4">
		<p class="text-xs text-primary-300">추천 캐릭터</p>
		<p class="text-lg font-bold">{featured.name}</p>
		<p class="text-xs text-text-muted">{featured.title}</p>
		<Button href="/mobile/chat/{featured.id}" size="sm" class="mt-3">
			<MessageCircle class="h-3.5 w-3.5" />
			대화 시작
		</Button>
	</div>
</section>

<section class="px-4">
	<h2 class="mb-3 text-sm font-semibold">최근 대화</h2>
	<div class="space-y-2">
		{#each recentChats as chat}
			<a
				href="/mobile/chat/{chat.id}"
				class="flex items-center gap-3 rounded-xl border border-white/10 bg-bg-surface/50 p-3"
			>
				<img
					src="https://api.dicebear.com/9.x/notionists/svg?seed={chat.id}"
					alt=""
					class="h-11 w-11 rounded-full bg-bg-card"
				/>
				<div class="min-w-0 flex-1">
					<div class="flex items-center justify-between">
						<p class="font-medium">{chat.name}</p>
						<span class="text-[10px] text-text-muted">{chat.time}</span>
					</div>
					<p class="truncate text-xs text-text-muted">{chat.preview}</p>
				</div>
			</a>
		{/each}
	</div>
</section>
