<script lang="ts">
	const phones = [
		{ id: 'M01', label: '홈', href: '/mobile/home' },
		{ id: 'M02', label: '탐색', href: '/mobile/explore' },
		{ id: 'M03', label: '채팅', href: '/mobile/chat/elia' },
		{ id: 'M04', label: '관계도', href: '/mobile/relationship' },
		{ id: 'M05', label: '기억', href: '/mobile/memory' },
		{ id: 'M06', label: '감정', href: '/mobile/emotion' },
		{ id: 'M07', label: '프로필', href: '/mobile/characters/elia' },
		{ id: 'M08', label: '마이페이지', href: '/mobile/profile' }
	];
</script>

<svelte:head>
	<title>Mobile Design — Screen 12</title>
</svelte:head>

<div class="min-h-screen bg-bg-primary p-6 lg:p-10">
	<div class="mx-auto max-w-7xl">
		<h1 class="text-2xl font-bold">Mobile Design</h1>
		<p class="mt-1 text-sm text-text-muted">Screen 12 · 360×800 · 8 phones</p>
		<p class="mt-2 text-sm text-text-secondary">
			<a href="/home" class="text-primary-400 hover:underline">← PC 버전</a>
		</p>

		<div class="mt-8 grid gap-8 sm:grid-cols-2 xl:grid-cols-4">
			{#each phones as phone}
				<a href={phone.href} class="group block">
					<div
						class="mx-auto aspect-[360/800] w-full max-w-[360px] overflow-hidden rounded-[2rem] border border-white/10 bg-bg-surface shadow-xl transition group-hover:border-primary-500/40"
					>
						<div class="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
							<span class="text-xs text-text-muted">{phone.id}</span>
							<span class="text-lg font-semibold">{phone.label}</span>
							<span class="text-xs text-primary-400">360 × 800 →</span>
						</div>
					</div>
				</a>
			{/each}
		</div>
	</div>
</div>
