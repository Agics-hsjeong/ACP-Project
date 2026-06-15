<script lang="ts">
	import type { ChatMessage } from '$lib/data/mock';

	interface Props {
		message: ChatMessage;
		characterName?: string;
	}

	let { message, characterName = '캐릭터' }: Props = $props();
</script>

{#if message.role === 'narration'}
	<p class="px-4 py-2 text-center text-sm italic text-primary-400">*{message.content}*</p>
{:else if message.role === 'system'}
	<p class="px-4 py-2 text-center text-xs text-accent-gold">{message.content}</p>
{:else if message.role === 'user'}
	<div class="flex justify-end px-4 py-1">
		<div class="max-w-[70%]">
			<div class="rounded-2xl rounded-br-md bg-primary-600 px-4 py-2.5 text-sm">
				{message.content}
				{#if message.timestamp}
					<p class="mt-1 text-right text-[10px] text-primary-200">{message.timestamp}</p>
				{/if}
			</div>
			{#if message.emotionDelta}
				<p class="mt-1 text-right text-[10px] text-accent-green">{message.emotionDelta}</p>
			{/if}
		</div>
	</div>
{:else}
	<div class="flex gap-3 px-4 py-1">
		<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-bg-card text-xs font-medium">
			{characterName[0]}
		</div>
		<div class="max-w-[70%]">
			<div class="rounded-2xl rounded-bl-md bg-bg-surface px-4 py-2.5 text-sm">
				<p class="mb-1 text-xs font-medium text-primary-300">{characterName}</p>
				<span>{message.content}</span>
				{#if message.isStreaming}
					<span class="ml-0.5 inline-block h-4 w-0.5 animate-pulse bg-primary-400 align-middle"></span>
				{/if}
				{#if message.timestamp && !message.isStreaming}
					<p class="mt-1 text-[10px] text-text-muted">{message.timestamp}</p>
				{/if}
			</div>
			{#if message.emotionDelta && !message.isStreaming}
				<p class="mt-1 text-[10px] text-accent-green">{message.emotionDelta}</p>
			{/if}
		</div>
	</div>
{/if}
