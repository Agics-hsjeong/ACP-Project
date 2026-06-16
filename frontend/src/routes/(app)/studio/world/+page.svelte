<script lang="ts">
	import { onMount } from 'svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { getStudioWorlds, initStudio, saveStudioWorld } from '$lib/stores/studio.svelte';
	import { Check, Eye } from 'lucide-svelte';

	const worlds = $derived(getStudioWorlds());

	let selectedWorldId = $state('');
	let saved = $state(true);
	let saving = $state(false);
	let toast = $state('');

	$effect(() => {
		if (!selectedWorldId && worlds.length) selectedWorldId = worlds[0].id;
	});

	const world = $derived(worlds.find((w) => w.id === selectedWorldId) ?? null);

	let name = $state('');
	let genreText = $state('');
	let cover = $state('');

	$effect(() => {
		if (!world) return;
		name = world.name;
		genreText = (world.genre ?? []).join(', ');
		cover = world.cover;
		saved = true;
	});

	onMount(() => {
		void initStudio();
	});

	function markDirty() {
		saved = false;
	}

	async function handleSave() {
		if (!world) return;
		saving = true;
		toast = '';
		try {
			await saveStudioWorld(world.id, {
				name,
				genre: genreText
					.split(',')
					.map((t) => t.trim())
					.filter(Boolean),
				cover
			});
			saved = true;
			toast = '저장되었습니다';
			setTimeout(() => (toast = ''), 2000);
		} catch (err) {
			toast = err instanceof Error ? err.message : '저장에 실패했습니다';
		} finally {
			saving = false;
		}
	}
</script>

<svelte:head>
	<title>세계관 스튜디오 — ACP</title>
</svelte:head>

<div class="mx-auto flex h-[calc(100dvh-0px)] min-h-[600px] max-w-6xl flex-col">
	<header class="flex flex-wrap items-center gap-3 border-b border-white/10 px-4 py-3">
		<div class="min-w-[220px]">
			<p class="text-xs text-text-muted">세계관 스튜디오 (실데이터)</p>
			<h1 class="text-lg font-bold">{world?.name ?? '로딩 중…'}</h1>
		</div>
		<div class="ml-auto flex flex-wrap items-center gap-2">
			{#if saved}
				<span class="flex items-center gap-1 text-xs text-accent-green">
					<Check class="h-3.5 w-3.5" /> 저장됨
				</span>
			{/if}
			<Button variant="secondary" class="gap-2" disabled>
				<Eye class="h-4 w-4" /> 미리보기
			</Button>
			<Button onclick={handleSave} disabled={saving || !world}>
				{saving ? '저장 중…' : '저장'}
			</Button>
		</div>
		{#if toast}
			<p class="w-full text-center text-xs text-text-muted">{toast}</p>
		{/if}
	</header>

	<div class="flex-1 overflow-y-auto p-4 lg:p-6">
		<div class="grid gap-6 lg:grid-cols-[240px_1fr]">
			<aside class="space-y-2 rounded-2xl border border-white/10 bg-bg-surface/40 p-3">
				<p class="px-1 text-xs text-text-muted">세계관 목록</p>
				{#each worlds as w}
					<button
						type="button"
						class="w-full rounded-xl px-3 py-2 text-left text-sm transition {selectedWorldId === w.id
							? 'bg-primary-600/20 text-primary-200'
							: 'text-text-secondary hover:bg-white/5 hover:text-text-primary'}"
						onclick={() => {
							selectedWorldId = w.id;
							saved = true;
						}}
					>
						<div class="flex items-center gap-2">
							<img src={w.cover} alt="" class="h-7 w-7 rounded-lg bg-bg-card object-cover" />
							<span class="truncate font-medium">{w.name}</span>
						</div>
					</button>
				{/each}
			</aside>

			<section class="min-w-0 space-y-4">
				{#if world}
					<div class="grid gap-4 md:grid-cols-2" oninput={markDirty} onchange={markDirty}>
						<Input label="이름" bind:value={name} />
						<Input label="커버 URL" bind:value={cover} />

						<div class="md:col-span-2">
							<Input label="장르 (콤마 구분)" bind:value={genreText} />
							<div class="mt-2 flex flex-wrap gap-2">
								{#each genreText.split(',').map((t)=>t.trim()).filter(Boolean) as g}
									<Badge label={g} variant="primary" />
								{/each}
							</div>
						</div>
					</div>
				{:else}
					<div class="rounded-2xl border border-white/10 bg-bg-surface/40 p-6 text-sm text-text-muted">
						데이터를 불러오는 중…
					</div>
				{/if}
			</section>
		</div>
	</div>
</div>
