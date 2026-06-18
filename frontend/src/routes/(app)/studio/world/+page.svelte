<script lang="ts">
	import { onMount } from 'svelte';
	import WorldListPanel from '$lib/components/studio/WorldListPanel.svelte';
	import StudioPanel from '$lib/components/studio/StudioPanel.svelte';
	import StudioTabBar from '$lib/components/studio/StudioTabBar.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import {
		worldStudioTabs,
		defaultWorldStudioMeta,
		type WorldTab,
		type WorldFaction,
		type WorldNation,
		type WorldLocation,
		type WorldEvent,
		type WorldLaw,
		type WorldMemo,
		type WorldEra,
		type WorldTheme,
		type WorldCulture
	} from '$lib/data/studio';
	import { parseWorldStudioMeta } from '$lib/studio/character';
	import { getStudioWorlds, initStudio, saveStudioWorld } from '$lib/stores/studio.svelte';
	import { Check, ChevronRight, Eye, Map, Plus, Trash2 } from 'lucide-svelte';

	const worlds = $derived(getStudioWorlds());

	let selectedWorldId = $state('');
	let activeTab = $state<WorldTab>('basic');
	let saved = $state(true);
	let saving = $state(false);
	let toast = $state('');

	let name = $state('');
	let genreText = $state('');
	let cover = $state('');
	let meta = $state(defaultWorldStudioMeta());

	const world = $derived(worlds.find((w) => w.id === selectedWorldId) ?? null);
	const breadcrumb = $derived(name ? `세계관 스튜디오 › ${name}` : '세계관 스튜디오');

	$effect(() => {
		if (!selectedWorldId && worlds.length) selectedWorldId = worlds[0].id;
	});

	$effect(() => {
		if (!world) return;
		name = world.name;
		genreText = (world.genre ?? []).join(', ');
		cover = world.cover;
		meta = parseWorldStudioMeta((world.studioMeta ?? {}) as Record<string, unknown>);
		saved = true;
	});

	onMount(() => {
		void initStudio();
	});

	function markDirty() {
		saved = false;
	}

	function newId(prefix: string) {
		return `${prefix}_${Math.random().toString(16).slice(2, 8)}${Date.now().toString(16).slice(-4)}`;
	}

	function addFaction() {
		meta = {
			...meta,
			factions: [
				...meta.factions,
				{ id: newId('faction'), name: '', alignment: '', description: '', power: 5, icon: '✨' }
			]
		};
		markDirty();
	}
	function removeFaction(id: string) {
		meta = { ...meta, factions: meta.factions.filter((f) => f.id !== id) };
		markDirty();
	}

	function addCulture() {
		meta = {
			...meta,
			cultures: [
				...meta.cultures,
				{ id: newId('culture'), name: '', region: '', traits: '', description: '' }
			]
		};
		markDirty();
	}
	function removeCulture(id: string) {
		meta = { ...meta, cultures: meta.cultures.filter((c) => c.id !== id) };
		markDirty();
	}

	function addNation() {
		meta = {
			...meta,
			nations: [
				...meta.nations,
				{ id: newId('nation'), name: '', capital: '', ruler: '', population: '', description: '' }
			]
		};
		markDirty();
	}
	function removeNation(id: string) {
		meta = { ...meta, nations: meta.nations.filter((n) => n.id !== id) };
		markDirty();
	}

	function addLocation() {
		meta = {
			...meta,
			locations: [
				...meta.locations,
				{ id: newId('loc'), name: '', type: '', region: '', description: '' }
			]
		};
		markDirty();
	}
	function removeLocation(id: string) {
		meta = { ...meta, locations: meta.locations.filter((l) => l.id !== id) };
		markDirty();
	}

	function addEvent() {
		meta = {
			...meta,
			events: [
				...meta.events,
				{ id: newId('ev'), year: 0, name: '', category: '', categoryColor: '#6366f1' }
			]
		};
		markDirty();
	}
	function removeEvent(id: string) {
		meta = { ...meta, events: meta.events.filter((e) => e.id !== id) };
		markDirty();
	}

	function addEra() {
		meta = {
			...meta,
			eras: [...meta.eras, { id: newId('era'), name: '', range: '', subtitle: '' }]
		};
		markDirty();
	}
	function removeEra(id: string) {
		meta = { ...meta, eras: meta.eras.filter((e) => e.id !== id) };
		markDirty();
	}

	function addTheme() {
		meta = { ...meta, themes: [...meta.themes, { id: newId('theme'), title: '', color: '#6366f1' }] };
		markDirty();
	}
	function removeTheme(id: string) {
		meta = { ...meta, themes: meta.themes.filter((t) => t.id !== id) };
		markDirty();
	}

	function addLaw() {
		meta = { ...meta, laws: [...meta.laws, { id: newId('law'), title: '', description: '', icon: '📜' }] };
		markDirty();
	}
	function removeLaw(id: string) {
		meta = { ...meta, laws: meta.laws.filter((l) => l.id !== id) };
		markDirty();
	}

	function addMemo() {
		meta = {
			...meta,
			memos: [
				...meta.memos,
				{ id: newId('memo'), title: '', content: '', updatedAt: new Date().toISOString().slice(0, 10) }
			]
		};
		markDirty();
	}
	function removeMemo(id: string) {
		meta = { ...meta, memos: meta.memos.filter((m) => m.id !== id) };
		markDirty();
	}

	function addGallery() {
		meta = { ...meta, gallery: [...meta.gallery, ''] };
		markDirty();
	}
	function removeGallery(index: number) {
		meta = { ...meta, gallery: meta.gallery.filter((_, i) => i !== index) };
		markDirty();
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
				cover,
				studio_meta: meta
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

	const sortedEvents = $derived([...meta.events].sort((a, b) => a.year - b.year));
</script>

<svelte:head>
	<title>세계관 스튜디오 — ACP</title>
</svelte:head>

<div class="flex min-h-0 flex-1 flex-col">
	<header class="shrink-0 border-b border-white/10 px-4 py-3 lg:px-6">
		<div class="flex flex-wrap items-center gap-3">
			<div class="min-w-0 flex-1">
				<p class="flex items-center gap-1 text-[11px] text-text-muted">
					<span>창작 스튜디오</span>
					<ChevronRight class="h-3 w-3" />
					<span class="text-text-secondary">{breadcrumb}</span>
				</p>
				<h1 class="mt-0.5 truncate text-lg font-bold">{name || '세계관 선택'}</h1>
			</div>
			<div class="flex flex-wrap items-center gap-2">
				{#if saved}
					<span class="flex items-center gap-1 text-xs text-accent-green">
						<Check class="h-3.5 w-3.5" /> 저장됨
					</span>
				{/if}
				<Button variant="secondary" class="gap-2" href="/explore" disabled={!world}>
					<Eye class="h-4 w-4" /> 미리보기
				</Button>
				<Button onclick={handleSave} disabled={saving || !world}>
					{saving ? '저장 중…' : '저장'}
				</Button>
			</div>
		</div>
		{#if toast}
			<p class="mt-2 text-center text-xs text-text-muted">{toast}</p>
		{/if}
	</header>

	<div class="grid min-h-0 flex-1 lg:grid-cols-[auto_1fr]">
		<WorldListPanel worlds={worlds} selectedId={selectedWorldId} onselect={(id) => {
			selectedWorldId = id;
			saved = true;
		}} />

		<section class="flex min-w-0 flex-col overflow-hidden">
			{#if world}
				<div class="shrink-0 border-b border-white/10 px-4 py-3 lg:px-6">
					<StudioTabBar tabs={worldStudioTabs} active={activeTab} onchange={(id) => (activeTab = id)} />
				</div>

				<div class="min-h-0 flex-1 overflow-y-auto p-4 lg:p-6" oninput={markDirty} onchange={markDirty}>
					{#if activeTab === 'basic'}
						<div class="grid gap-4 lg:grid-cols-3">
							<StudioPanel title="세계 지도" class="lg:col-span-1">
								<div class="overflow-hidden rounded-xl border border-white/10 bg-bg-primary/40">
									{#if meta.map_image}
										<img src={meta.map_image} alt="세계 지도" class="aspect-video w-full object-cover" />
									{:else}
										<div class="flex aspect-video items-center justify-center text-text-muted">
											<Map class="h-10 w-10 opacity-40" />
										</div>
									{/if}
								</div>
								<Input label="지도 이미지 URL" bind:value={meta.map_image} class="mt-3" />
							</StudioPanel>

							<StudioPanel title="기본 설정" class="lg:col-span-1">
								<div class="space-y-3">
									<Input label="세계관 이름" bind:value={name} />
									<Input label="커버 URL" bind:value={cover} />
									<Input label="시대 배경" bind:value={meta.era_setting} placeholder="예: 중세 판타지, AD 1500~" />
									<Input label="기술 수준" bind:value={meta.tech_level} placeholder="예: 검과 마법, 초기 화약" />
									<Input label="마법 체계" bind:value={meta.magic_system} placeholder="예: 마나 기반 원소 마법" />
									<Input label="분위기" bind:value={meta.atmosphere} placeholder="예: 장엄하고 서정적인" />
									<Input label="장르 (콤마 구분)" bind:value={genreText} />
								</div>
							</StudioPanel>

							<StudioPanel title="세계관 요약" class="lg:col-span-1">
								<Input label="한 줄 소개" bind:value={meta.one_liner} />
								<div class="mt-3">
									<label for="world-desc" class="text-sm text-text-secondary">상세 설명</label>
									<textarea
										id="world-desc"
										bind:value={meta.description}
										rows="8"
										class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"
									></textarea>
								</div>
								<div class="mt-3 flex flex-wrap gap-2">
									{#each genreText.split(',').map((t) => t.trim()).filter(Boolean) as g}
										<Badge label={g} variant="primary" />
									{/each}
								</div>
							</StudioPanel>
						</div>

						<div class="mt-4 grid gap-4 lg:grid-cols-3">
							<StudioPanel title="지리 · 지역">
								<p class="mb-2 text-xs text-text-muted">{meta.locations.length}개 장소 · {meta.nations.length}개 국가</p>
								<ul class="space-y-1 text-sm text-text-secondary">
									{#each meta.locations.slice(0, 4) as loc}
										<li>· {loc.name || '이름 없음'} <span class="text-text-muted">({loc.region})</span></li>
									{:else}
										<li class="text-text-muted">등록된 장소가 없습니다.</li>
									{/each}
								</ul>
								<button type="button" class="mt-3 text-xs text-primary-400 hover:underline" onclick={() => (activeTab = 'geography')}>
									지리 편집 →
								</button>
							</StudioPanel>
							<StudioPanel title="종족 · 문화">
								<p class="mb-2 text-xs text-text-muted">{meta.cultures.length}개 문화 · {meta.factions.length}개 세력</p>
								<ul class="space-y-1 text-sm text-text-secondary">
									{#each meta.cultures.slice(0, 3) as c}
										<li>· {c.name || '문화'} — {c.traits || '특성 미설정'}</li>
									{:else}
										{#each meta.factions.slice(0, 3) as f}
											<li>· {f.icon} {f.name || '세력'}</li>
										{:else}
											<li class="text-text-muted">등록된 문화가 없습니다.</li>
										{/each}
									{/each}
								</ul>
								<button type="button" class="mt-3 text-xs text-primary-400 hover:underline" onclick={() => (activeTab = 'culture')}>
									문화 편집 →
								</button>
							</StudioPanel>
							<StudioPanel title="역사 · 사건">
								<p class="mb-2 text-xs text-text-muted">{meta.events.length}개 사건 · {meta.eras.length}개 시대</p>
								<ul class="space-y-1 text-sm text-text-secondary">
									{#each sortedEvents.slice(0, 4) as ev}
										<li>
											<span class="text-primary-300">{ev.year > 0 ? `AD ${ev.year}` : `BC ${Math.abs(ev.year)}`}</span>
											· {ev.name || '사건'}
										</li>
									{:else}
										<li class="text-text-muted">등록된 사건이 없습니다.</li>
									{/each}
								</ul>
								<button type="button" class="mt-3 text-xs text-primary-400 hover:underline" onclick={() => (activeTab = 'history')}>
									역사 편집 →
								</button>
							</StudioPanel>
						</div>

						<div class="mt-4">
							<StudioPanel title="갤러리">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addGallery}>
										<Plus class="h-4 w-4" /> 이미지 추가
									</Button>
								</div>
								<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
									{#each meta.gallery as url, i}
										<div class="space-y-2">
											{#if url}
												<img src={url} alt="" class="aspect-video w-full rounded-xl border border-white/10 object-cover" />
											{:else}
												<div class="aspect-video rounded-xl border border-dashed border-white/10 bg-bg-primary/30"></div>
											{/if}
											<div class="flex gap-1">
												<input
													value={url}
													placeholder="이미지 URL"
													class="h-8 flex-1 rounded-lg border border-white/10 bg-bg-primary/60 px-2 text-xs outline-none focus:border-primary-500"
													oninput={(e) => {
														meta = {
															...meta,
															gallery: meta.gallery.map((u, idx) =>
																idx === i ? (e.currentTarget as HTMLInputElement).value : u
															)
														};
														markDirty();
													}}
												/>
												<button
													type="button"
													class="rounded-lg p-2 text-text-muted hover:text-accent-red"
													onclick={() => removeGallery(i)}
												>
													<Trash2 class="h-3.5 w-3.5" />
												</button>
											</div>
										</div>
									{/each}
								</div>
							</StudioPanel>
						</div>
					{:else if activeTab === 'geography'}
						<div class="mb-4 flex items-center justify-between">
							<p class="text-sm text-text-muted">지도, 국가, 장소를 설정합니다.</p>
						</div>
						<div class="mb-4">
							<StudioPanel title="세계 지도">
								<div class="grid gap-4 lg:grid-cols-2">
									<div class="overflow-hidden rounded-xl border border-white/10">
										{#if meta.map_image}
											<img src={meta.map_image} alt="" class="max-h-64 w-full object-cover" />
										{/if}
									</div>
									<Input label="지도 이미지 URL" bind:value={meta.map_image} />
								</div>
							</StudioPanel>
						</div>

						<div class="mb-3 flex items-center justify-between">
							<h3 class="text-sm font-semibold">국가</h3>
							<Button size="sm" variant="secondary" onclick={addNation}>
								<Plus class="h-4 w-4" /> 국가 추가
							</Button>
						</div>
						<div class="mb-6 grid gap-3 lg:grid-cols-2">
							{#each meta.nations as nation (nation.id)}
								<StudioPanel title={nation.name || '새 국가'}>
									{#snippet actions()}
										<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeNation(nation.id)}>
											<Trash2 class="h-4 w-4" />
										</button>
									{/snippet}
									<div class="grid gap-3 sm:grid-cols-2">
										<Input label="이름" bind:value={nation.name} />
										<Input label="수도" bind:value={nation.capital} />
										<Input label="통치자" bind:value={nation.ruler} />
										<Input label="인구" bind:value={nation.population} />
										<div class="sm:col-span-2">
											<label for="nation-{nation.id}" class="text-sm text-text-secondary">설명</label>
											<textarea id="nation-{nation.id}" bind:value={nation.description} rows="3" class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"></textarea>
										</div>
									</div>
								</StudioPanel>
							{:else}
								<p class="text-sm text-text-muted">등록된 국가가 없습니다.</p>
							{/each}
						</div>

						<div class="mb-3 flex items-center justify-between">
							<h3 class="text-sm font-semibold">장소</h3>
							<Button size="sm" variant="secondary" onclick={addLocation}>
								<Plus class="h-4 w-4" /> 장소 추가
							</Button>
						</div>
						<div class="grid gap-3 lg:grid-cols-2">
							{#each meta.locations as loc (loc.id)}
								<StudioPanel title={loc.name || '새 장소'}>
									{#snippet actions()}
										<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeLocation(loc.id)}>
											<Trash2 class="h-4 w-4" />
										</button>
									{/snippet}
									<div class="grid gap-3 sm:grid-cols-2">
										<Input label="이름" bind:value={loc.name} />
										<Input label="유형" bind:value={loc.type} placeholder="성, 숲, 도시…" />
										<Input label="지역" bind:value={loc.region} class="sm:col-span-2" />
										<div class="sm:col-span-2">
											<label for="loc-{loc.id}" class="text-sm text-text-secondary">설명</label>
											<textarea id="loc-{loc.id}" bind:value={loc.description} rows="3" class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"></textarea>
										</div>
									</div>
								</StudioPanel>
							{:else}
								<p class="text-sm text-text-muted">등록된 장소가 없습니다.</p>
							{/each}
						</div>
					{:else if activeTab === 'culture'}
						<div class="mb-3 flex items-center justify-between">
							<h3 class="text-sm font-semibold">종족 · 문화</h3>
							<Button size="sm" variant="secondary" onclick={addCulture}>
								<Plus class="h-4 w-4" /> 문화 추가
							</Button>
						</div>
						<div class="mb-6 grid gap-3 lg:grid-cols-2">
							{#each meta.cultures as culture (culture.id)}
								<StudioPanel title={culture.name || '새 문화'}>
									{#snippet actions()}
										<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeCulture(culture.id)}>
											<Trash2 class="h-4 w-4" />
										</button>
									{/snippet}
									<div class="grid gap-3">
										<Input label="종족 / 문화명" bind:value={culture.name} />
										<Input label="거주 지역" bind:value={culture.region} />
										<Input label="특성 (콤마 구분)" bind:value={culture.traits} placeholder="예: 수명이 길고, 자연 친화적" />
										<div>
											<label for="culture-{culture.id}" class="text-sm text-text-secondary">설명</label>
											<textarea id="culture-{culture.id}" bind:value={culture.description} rows="3" class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"></textarea>
										</div>
									</div>
								</StudioPanel>
							{:else}
								<p class="col-span-2 text-sm text-text-muted">등록된 문화가 없습니다. 아래 세력도 함께 관리할 수 있습니다.</p>
							{/each}
						</div>

						<div class="mb-3 flex items-center justify-between">
							<h3 class="text-sm font-semibold">세력 · 팩션</h3>
							<Button size="sm" variant="secondary" onclick={addFaction}>
								<Plus class="h-4 w-4" /> 세력 추가
							</Button>
						</div>
						<div class="grid gap-3 lg:grid-cols-2">
							{#each meta.factions as faction (faction.id)}
								<StudioPanel>
									<div class="mb-3 flex items-center justify-between">
										<div class="flex items-center gap-2">
											<span class="text-xl">{faction.icon}</span>
											<span class="font-semibold">{faction.name || '새 세력'}</span>
										</div>
										<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeFaction(faction.id)}>
											<Trash2 class="h-4 w-4" />
										</button>
									</div>
									<div class="mb-3 h-2 overflow-hidden rounded-full bg-bg-primary/80">
										<div class="h-full rounded-full bg-gradient-to-r from-primary-600 to-primary-400" style="width: {Math.min(100, faction.power)}%"></div>
									</div>
									<div class="grid gap-3 sm:grid-cols-2">
										<Input label="이름" bind:value={faction.name} />
										<Input label="아이콘" bind:value={faction.icon} />
										<Input label="성향" bind:value={faction.alignment} />
										<Input label="세력 (1~100)" type="number" bind:value={faction.power} />
										<div class="sm:col-span-2">
											<label for="faction-{faction.id}" class="text-sm text-text-secondary">설명</label>
											<textarea id="faction-{faction.id}" bind:value={faction.description} rows="3" class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"></textarea>
										</div>
									</div>
								</StudioPanel>
							{/each}
						</div>
					{:else if activeTab === 'history'}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="연대표 · 시대">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addEra}>
										<Plus class="h-4 w-4" /> 시대 추가
									</Button>
								</div>
								<div class="relative space-y-0 border-l border-primary-500/30 pl-4">
									{#each meta.eras as era (era.id)}
										<div class="relative pb-4">
											<div class="absolute -left-[21px] top-1 h-2.5 w-2.5 rounded-full bg-primary-500 ring-4 ring-bg-surface"></div>
											<div class="flex items-start justify-between gap-2">
												<div>
													<p class="text-sm font-semibold">{era.name || '시대'}</p>
													<p class="text-xs text-primary-300">{era.range}</p>
													<p class="text-xs text-text-muted">{era.subtitle}</p>
												</div>
												<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeEra(era.id)}>
													<Trash2 class="h-3.5 w-3.5" />
												</button>
											</div>
											<div class="mt-2 grid gap-2 sm:grid-cols-3">
												<Input label="이름" bind:value={era.name} />
												<Input label="범위" bind:value={era.range} />
												<Input label="부제" bind:value={era.subtitle} />
											</div>
										</div>
									{:else}
										<p class="text-sm text-text-muted">등록된 시대가 없습니다.</p>
									{/each}
								</div>
							</StudioPanel>

							<StudioPanel title="핵심 테마">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addTheme}>
										<Plus class="h-4 w-4" /> 테마 추가
									</Button>
								</div>
								<div class="space-y-2">
									{#each meta.themes as theme (theme.id)}
										<div class="flex items-center gap-2 rounded-xl border border-white/10 bg-bg-primary/30 p-3">
											<div class="h-3 w-3 shrink-0 rounded-full" style="background: {theme.color}"></div>
											<input bind:value={theme.title} placeholder="테마 제목" class="h-9 flex-1 rounded-lg border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none focus:border-primary-500" />
											<input bind:value={theme.color} class="h-9 w-24 rounded-lg border border-white/10 bg-bg-primary/60 px-2 text-xs outline-none focus:border-primary-500" />
											<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeTheme(theme.id)}>
												<Trash2 class="h-4 w-4" />
											</button>
										</div>
									{/each}
								</div>
							</StudioPanel>
						</div>

						<div class="mt-4">
							<StudioPanel title="역사 · 사건">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addEvent}>
										<Plus class="h-4 w-4" /> 사건 추가
									</Button>
								</div>
								<div class="space-y-2">
									{#each sortedEvents as ev (ev.id)}
										<div class="flex flex-wrap items-center gap-3 rounded-xl border border-white/10 bg-bg-primary/30 p-3">
											<span class="w-20 shrink-0 text-xs font-medium text-primary-300">
												{ev.year > 0 ? `AD ${ev.year}` : `BC ${Math.abs(ev.year)}`}
											</span>
											<span class="rounded-full px-2 py-0.5 text-[10px] font-medium" style="background: {ev.categoryColor}22; color: {ev.categoryColor}">
												{ev.category || '분류'}
											</span>
											<input bind:value={ev.name} placeholder="사건명" class="h-9 min-w-[120px] flex-1 rounded-lg border border-white/10 bg-bg-primary/60 px-3 text-sm outline-none focus:border-primary-500" />
											<input bind:value={ev.category} placeholder="카테고리" class="h-9 w-24 rounded-lg border border-white/10 bg-bg-primary/60 px-2 text-xs outline-none focus:border-primary-500" />
											<input type="number" bind:value={ev.year} class="h-9 w-24 rounded-lg border border-white/10 bg-bg-primary/60 px-2 text-xs outline-none focus:border-primary-500" />
											<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeEvent(ev.id)}>
												<Trash2 class="h-4 w-4" />
											</button>
										</div>
									{:else}
										<p class="text-sm text-text-muted">등록된 사건이 없습니다.</p>
									{/each}
								</div>
							</StudioPanel>
						</div>
					{:else if activeTab === 'rules'}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="마법 · 규칙 체계">
								<div class="space-y-3">
									<div>
										<label for="magic-sys" class="text-sm text-text-secondary">마법 체계 상세</label>
										<textarea id="magic-sys" bind:value={meta.magic_system} rows="5" class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500" placeholder="마나, 원소, 금기, 역효과 등…"></textarea>
									</div>
								</div>
							</StudioPanel>
							<StudioPanel title="제작 메모">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addMemo}>
										<Plus class="h-4 w-4" /> 메모 추가
									</Button>
								</div>
								<div class="space-y-3">
									{#each meta.memos as memo (memo.id)}
										<div class="rounded-xl border border-white/10 bg-bg-primary/30 p-3">
											<div class="mb-2 flex items-center justify-between">
												<input bind:value={memo.title} placeholder="제목" class="flex-1 bg-transparent text-sm font-semibold outline-none" />
												<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeMemo(memo.id)}>
													<Trash2 class="h-4 w-4" />
												</button>
											</div>
											<textarea bind:value={memo.content} rows="3" class="w-full rounded-lg border border-white/10 bg-bg-primary/60 px-3 py-2 text-sm outline-none focus:border-primary-500"></textarea>
											<input bind:value={memo.updatedAt} class="mt-2 h-8 w-full rounded-lg border border-white/10 bg-bg-primary/60 px-2 text-xs outline-none focus:border-primary-500" />
										</div>
									{/each}
								</div>
							</StudioPanel>
						</div>

						<div class="mt-4">
							<StudioPanel title="절대 법칙">
								<div class="mb-3 flex justify-end">
									<Button size="sm" variant="secondary" onclick={addLaw}>
										<Plus class="h-4 w-4" /> 법칙 추가
									</Button>
								</div>
								<div class="grid gap-3 lg:grid-cols-2">
									{#each meta.laws as law (law.id)}
										<div class="rounded-xl border border-white/10 bg-bg-primary/30 p-4">
											<div class="mb-3 flex items-center justify-between">
												<div class="flex items-center gap-2">
													<span class="text-xl">{law.icon}</span>
													<span class="font-semibold">{law.title || '새 법칙'}</span>
												</div>
												<button type="button" class="rounded p-1 text-text-muted hover:text-accent-red" onclick={() => removeLaw(law.id)}>
													<Trash2 class="h-4 w-4" />
												</button>
											</div>
											<div class="grid gap-3 sm:grid-cols-2">
												<Input label="아이콘" bind:value={law.icon} />
												<Input label="제목" bind:value={law.title} />
												<div class="sm:col-span-2">
													<label for="law-{law.id}" class="text-sm text-text-secondary">설명</label>
													<textarea id="law-{law.id}" bind:value={law.description} rows="3" class="mt-1.5 w-full rounded-xl border border-white/10 bg-bg-primary/60 px-4 py-3 text-sm outline-none focus:border-primary-500"></textarea>
												</div>
											</div>
										</div>
									{:else}
										<p class="text-sm text-text-muted">등록된 법칙이 없습니다.</p>
									{/each}
								</div>
							</StudioPanel>
						</div>
					{:else}
						<div class="grid gap-4 lg:grid-cols-2">
							<StudioPanel title="세계관 카드">
								<div class="flex gap-4">
									<img src={cover} alt="" class="h-24 w-24 rounded-2xl object-cover" />
									<div>
										<p class="text-xl font-bold">{name}</p>
										<p class="text-sm text-text-muted">{meta.one_liner}</p>
										<div class="mt-2 flex flex-wrap gap-1.5">
											{#each genreText.split(',').map((t) => t.trim()).filter(Boolean) as g}
												<Badge label={g} variant="primary" />
											{/each}
										</div>
									</div>
								</div>
								<p class="mt-4 text-sm leading-relaxed text-text-secondary">{meta.description}</p>
								<div class="mt-4 grid grid-cols-2 gap-2 text-xs text-text-muted">
									<span>시대: {meta.era_setting || '—'}</span>
									<span>기술: {meta.tech_level || '—'}</span>
									<span>마법: {meta.magic_system || '—'}</span>
									<span>분위기: {meta.atmosphere || '—'}</span>
								</div>
							</StudioPanel>
							<StudioPanel title="세계 지도">
								{#if meta.map_image}
									<img src={meta.map_image} alt="" class="w-full rounded-xl border border-white/10 object-cover" />
								{:else}
									<div class="flex h-48 items-center justify-center rounded-xl border border-dashed border-white/10 text-text-muted">
										지도 미설정
									</div>
								{/if}
							</StudioPanel>
						</div>
						<div class="mt-4 grid gap-4 lg:grid-cols-3">
							<StudioPanel title="국가 ({meta.nations.length})">
								<ul class="space-y-1 text-sm text-text-secondary">
									{#each meta.nations as n}
										<li>· {n.name} — {n.capital}</li>
									{/each}
								</ul>
							</StudioPanel>
							<StudioPanel title="세력 ({meta.factions.length})">
								<ul class="space-y-1 text-sm text-text-secondary">
									{#each meta.factions as f}
										<li>{f.icon} {f.name}</li>
									{/each}
								</ul>
							</StudioPanel>
							<StudioPanel title="사건 ({meta.events.length})">
								<ul class="space-y-1 text-sm text-text-secondary">
									{#each sortedEvents.slice(0, 5) as ev}
										<li>{ev.year}: {ev.name}</li>
									{/each}
								</ul>
							</StudioPanel>
						</div>
					{/if}
				</div>
			{:else}
				<div class="flex flex-1 items-center justify-center p-6">
					<div class="rounded-2xl border border-white/10 bg-bg-surface/40 p-8 text-center text-sm text-text-muted">
						세계관 데이터를 불러오는 중…
					</div>
				</div>
			{/if}
		</section>
	</div>
</div>
