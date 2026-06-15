<script lang="ts">
	import { page } from '$app/stores';
	import { getCharacter } from '$lib/data/mock';
	import { getChatMessages, sendChatMessage, isCharacterReplying } from '$lib/stores/chat.svelte';
	import { autoscroll } from '$lib/actions/autoscroll';
	import ChatBubble from '$lib/components/chat/ChatBubble.svelte';
	import ChatSessionPanel from '$lib/components/chat/ChatSessionPanel.svelte';
	import ChatEmotionPanel from '$lib/components/chat/ChatEmotionPanel.svelte';
	import ChatInteractionBar from '$lib/components/chat/ChatInteractionBar.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { Send, Bookmark, MoreHorizontal, Heart } from 'lucide-svelte';

	const character = $derived(getCharacter($page.params.id) ?? getCharacter('elia')!);
	let input = $state('');

	const messages = $derived(getChatMessages(character.id));
	const replying = $derived(isCharacterReplying(character.id));

	function handleSubmit(e: Event) {
		e.preventDefault();
		if (!input.trim() || replying) return;
		sendChatMessage(character.id, character.name, input);
		input = '';
	}
</script>

<svelte:head>
	<title>{character.name}와의 대화 — ACP</title>
</svelte:head>

<div class="flex h-[calc(100dvh-0px)] lg:h-[calc(100vh-0px)]">
	<ChatSessionPanel activeId={character.id} />

	<div class="flex min-w-0 flex-1 flex-col border-x border-white/10 bg-bg-primary/50">
		<header class="flex items-center gap-4 border-b border-white/10 bg-bg-surface/40 px-4 py-3 backdrop-blur-sm">
			<img src={character.avatar} alt="" class="h-11 w-11 rounded-full border-2 border-primary-500/30 bg-bg-card" />
			<div class="min-w-0 flex-1">
				<div class="flex items-center gap-2">
					<p class="font-semibold">{character.name}</p>
					<span class="rounded bg-primary-500/20 px-1.5 py-0.5 text-[10px] text-primary-300">✓</span>
				</div>
				<p class="truncate text-xs text-text-muted">
					{character.age ? `${character.age}세 · ` : ''}{character.gender ?? ''} · {character.occupation} ·
					{character.world}
				</p>
			</div>
			<div class="flex items-center gap-1">
				<button class="rounded-lg p-2 text-text-muted hover:bg-white/5" aria-label="즐겨찾기">
					<Bookmark class="h-4 w-4" />
				</button>
				<a
					href="/emotion"
					class="rounded-lg p-2 text-text-muted hover:bg-white/5 xl:hidden"
					aria-label="감정"
				>
					<Heart class="h-4 w-4" />
				</a>
				<button class="rounded-lg p-2 text-text-muted hover:bg-white/5" aria-label="더보기">
					<MoreHorizontal class="h-4 w-4" />
				</button>
			</div>
		</header>

		<div
			use:autoscroll
			class="relative flex-1 space-y-3 overflow-y-auto bg-cover bg-center py-4"
			style="background-image: linear-gradient(rgba(15,23,42,0.88), rgba(15,23,42,0.92)), url('{character.cover}')"
		>
			{#each messages as message (message.id)}
				<ChatBubble {message} characterName={character.name} />
			{/each}
		</div>

		<footer class="border-t border-white/10 bg-bg-surface/60 p-4 backdrop-blur-sm">
			<ChatInteractionBar
				characterId={character.id}
				characterName={character.name}
				disabled={replying}
			/>
			<form class="mt-3 flex items-end gap-2" onsubmit={handleSubmit}>
				<textarea
					bind:value={input}
					rows="1"
					placeholder="메시지를 입력하세요... (*지문*은 나레이션으로 표시)"
					disabled={replying}
					class="max-h-32 min-h-11 flex-1 resize-none rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-2.5 text-sm outline-none focus:border-primary-500 disabled:opacity-50"
					onkeydown={(e) => {
						if (e.key === 'Enter' && !e.shiftKey) {
							e.preventDefault();
							handleSubmit(e);
						}
					}}
				></textarea>
				<Button type="submit" disabled={!input.trim() || replying}>
					<Send class="h-4 w-4" />
				</Button>
			</form>
			{#if replying}
				<p class="mt-2 text-center text-[10px] text-primary-300">응답 생성 중…</p>
			{/if}
		</footer>
	</div>

	<ChatEmotionPanel characterId={character.id} />
</div>
