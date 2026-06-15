<script lang="ts">
	import { page } from '$app/stores';
	import { tick } from 'svelte';
	import { getCharacter } from '$lib/data/mock';
	import { getChatMessages, sendChatMessage, isCharacterReplying } from '$lib/stores/chat.svelte';
	import { autoscroll } from '$lib/actions/autoscroll';
	import ChatBubble from '$lib/components/chat/ChatBubble.svelte';
	import ChatInteractionBar from '$lib/components/chat/ChatInteractionBar.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import { Send } from 'lucide-svelte';

	const character = $derived(getCharacter($page.params.id) ?? getCharacter('elia')!);
	let input = $state('');
	const messages = $derived(getChatMessages(character.id));
	const replying = $derived(isCharacterReplying(character.id));
</script>

<svelte:head>
	<title>{character.name} — Mobile Chat</title>
</svelte:head>

<header class="flex items-center gap-3 border-b border-white/10 px-4 py-3">
	<img src={character.avatar} alt="" class="h-10 w-10 rounded-full bg-bg-card" />
	<div class="flex-1">
		<p class="font-semibold">{character.name}</p>
		<p class="text-[10px] text-accent-green">● 온라인</p>
	</div>
</header>

<div
	use:autoscroll
	class="flex-1 space-y-2 overflow-y-auto px-3 py-4"
	style="min-height: calc(100dvh - 180px); background: linear-gradient(rgba(15,23,42,0.9), rgba(15,23,42,0.95)), url('{character.cover}') center/cover"
>
	{#each messages as message (message.id)}
		<ChatBubble {message} characterName={character.name} />
	{/each}
</div>

<form
	class="border-t border-white/10 p-3"
	onsubmit={(e) => {
		e.preventDefault();
		if (!input.trim() || replying) return;
		sendChatMessage(character.id, character.name, input);
		input = '';
	}}
>
	<ChatInteractionBar
		characterId={character.id}
		characterName={character.name}
		disabled={replying}
	/>
	<div class="mt-2 flex gap-2">
		<input
			bind:value={input}
			placeholder="메시지 입력..."
			disabled={replying}
			class="min-h-10 flex-1 rounded-xl border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none disabled:opacity-50"
		/>
		<Button type="submit" disabled={!input.trim() || replying}>
			<Send class="h-4 w-4" />
		</Button>
	</div>
</form>
