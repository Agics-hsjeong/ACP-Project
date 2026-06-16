<script lang="ts">
	import { onMount } from 'svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { getStudioCharacters, getStudioWorlds, initStudio, saveStudioCharacter } from '$lib/stores/studio.svelte';
	import { Check, Eye } from 'lucide-svelte';

	const characters = $derived(getStudioCharacters());
	const worlds = $derived(getStudioWorlds());

	let selectedId = $state('');
	let saved = $state(true);
	let saving = $state(false);
	let toast = $state('');

	$effect(() => {
		if (!selectedId && characters.length) selectedId = characters[0].id;
	});

	const character = $derived(characters.find((c) => c.id === selectedId) ?? null);

	let name = $state('');
	let title = $state('');
	let worldId = $state('');
	let description = $state('');
	let tagsText = $state('');
	let genreText = $state('');
	let avatar = $state('');
	let cover = $state('');

	$effect(() => {
		if (!character) return;
		name = character.name;
		title = character.title;
		worldId = character.worldId ?? worlds[0]?.id ?? 'arcadia';
		description = character.description;
		tagsText = (character.tags ?? []).join(', ');
		genreText = (character.genre ?? []).join(', ');
		avatar = character.avatar;
		cover = character.cover;
		saved = true;
	});

	onMount(() => {
		void initStudio();
	});

	function markDirty() {
		saved = false;
	}

	async function handleSave() {
		if (!character) return;
		saving = true;
		toast = '';
		try {
			await saveStudioCharacter(character.id, {
				name,
				title,
				world_id: worldId,
				description,
				tags: tagsText
					.split(',')
					.map((t) => t.trim())
					.filter(Boolean),
				genre: genreText
					.split(',')
					.map((t) => t.trim())
					.filter(Boolean),
				avatar,
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
	<title>캐릭터 스튜디오 — ACP</title>
</svelte:head>

<div class="mx-auto flex h-[calc(100dvh-0px)] min-h-[600px] max-w-6xl flex-col">
	<header class="flex flex-wrap items-center gap-3 border-b border-white/10 px-4 py-3">
		<div class="min-w-[220px]">
			<p class="text-xs text-text-muted">캐릭터 스튜디오 (실데이터)</p>
			<h1 class="text-lg font-bold">{character?.name ?? '로딩 중…'}</h1>
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
			<Button onclick={handleSave} disabled={saving || !character}>
				{saving ? '저장 중…' : '저장'}
			</Button>
		</div>
		{#if toast}
			<p class="w-full text-center text-xs text-text-muted">{toast}</p>
		{/if}
	</header>

	<div class="grid min-h-0 flex-1 gap-6 p-4 lg:grid-cols-[240px_1fr]">
		<aside class="space-y-2 rounded-2xl border border-white/10 bg-bg-surface/40 p-3">
			<p class="px-1 text-xs text-text-muted">캐릭터 목록</p>
			{#each characters as c}
				<button
					type="button"
					class="w-full rounded-xl px-3 py-2 text-left text-sm transition {selectedId === c.id
						? 'bg-primary-600/20 text-primary-200'
						: 'text-text-secondary hover:bg-white/5 hover:text-text-primary'}"
					onclick={() => {
						selectedId = c.id;
						saved = true;
					}}
				>
					<div class="flex items-center gap-2">
						<img src={c.avatar} alt="" class="h-7 w-7 rounded-lg bg-bg-card object-cover" />
						<span class="truncate font-medium">{c.name}</span>
					</div>
				</button>
			{/each}
		</aside>

		<section class="min-w-0 space-y-4">
			{#if character}
				<div class="grid gap-4 md:grid-cols-2" oninput={markDirty} onchange={markDirty}>
					<Input label="이름" bind:value={name} />
					<Input label="타이틀" bind:value={title} />

					<div class="flex flex-col gap-1.5">
						<label for="world" class="text-sm text-text-secondary">세계관</label>
						<select
							id="world"
							bind:value={worldId}
							class="h-11 rounded-xl border border-white/10 bg-bg-primary/60 px-4 text-sm outline-none focus:border-primary-500"
						>
							{#each worlds as w}
								<option value={w.id}>{w.name}</option>
							{/each}
						</select>
					</div>

					<Input label="아바타 URL" bind:value={avatar} />
					<div class="md:col-span-2">
						<Input label="커버 URL" bind:value={cover} />
					</div>

					<div class="md:col-span-2">
						<label for="desc" class="text-sm text-text-secondary">설명</label>
						<textarea
							id="desc"
							bind:value={description}
							rows="5"
							class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
						></textarea>
					</div>

					<div class="md:col-span-2">
						<Input label="태그 (콤마 구분)" bind:value={tagsText} />
						<div class="mt-2 flex flex-wrap gap-2">
							{#each tagsText.split(',').map((t)=>t.trim()).filter(Boolean) as t}
								<Badge label={t} variant="primary" />
							{/each}
						</div>
					</div>

					<div class="md:col-span-2">
						<Input label="장르 (콤마 구분)" bind:value={genreText} />
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
