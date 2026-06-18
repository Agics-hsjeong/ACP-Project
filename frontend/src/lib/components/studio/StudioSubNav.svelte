<script lang="ts">
	import { page } from '$app/stores';
	import { Palette, Globe, Zap, Package } from 'lucide-svelte';

	const items = [
		{ href: '/studio/character', label: '캐릭터', icon: Palette },
		{ href: '/studio/world', label: '세계관', icon: Globe },
		{ href: '/studio/event', label: '사건', icon: Zap, disabled: true },
		{ href: '/studio/item', label: '아이템', icon: Package, disabled: true }
	] as const;
</script>

<aside class="hidden w-52 shrink-0 flex-col border-r border-white/10 bg-bg-surface/30 xl:flex">
	<div class="border-b border-white/10 px-4 py-4">
		<p class="text-xs font-semibold text-text-primary">창작 스튜디오</p>
		<p class="mt-0.5 text-[10px] text-text-muted">캐릭터 · 세계관 제작</p>
	</div>
	<nav class="flex-1 space-y-0.5 p-2">
		{#each items as item}
			{@const active = $page.url.pathname.startsWith(item.href)}
			{#if item.disabled}
				<span
					class="flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-xs text-text-muted/50"
					title="준비 중"
				>
					<item.icon class="h-4 w-4 shrink-0" />
					{item.label}
					<span class="ml-auto text-[9px]">Soon</span>
				</span>
			{:else}
				<a
					href={item.href}
					class="flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-xs transition {active
						? 'bg-primary-600/20 font-medium text-primary-200 ring-1 ring-primary-500/30'
						: 'text-text-secondary hover:bg-white/5 hover:text-text-primary'}"
				>
					<item.icon class="h-4 w-4 shrink-0" />
					{item.label}
				</a>
			{/if}
		{/each}
	</nav>
</aside>
