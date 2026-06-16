<script lang="ts">
	import { goto } from '$app/navigation';
	import { getUser, logout } from '$lib/stores/auth.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';

	const user = $derived(getUser());
	let email = $state('creator@acp.local');
	let notifications = $state(true);
	let memoryAutoSave = $state(true);

	const displayEmail = $derived(user?.email ?? email);

	function handleLogout() {
		logout();
		goto('/login');
	}
</script>

<svelte:head>
	<title>설정 — ACP</title>
</svelte:head>

<div class="mx-auto max-w-lg space-y-6">
	<h1 class="text-2xl font-bold">설정</h1>

	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="font-semibold">계정</h2>
		<p class="mt-1 text-xs text-text-muted">로그인: {user?.name ?? 'Guest'} ({displayEmail})</p>
		<div class="mt-4 space-y-3">
			<Input label="이메일" type="email" bind:value={email} />
			<Button variant="secondary" size="sm">비밀번호 변경</Button>
		</div>
	</section>

	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="mb-4 font-semibold">알림</h2>
		<label class="flex items-center justify-between text-sm">
			<span>푸시 알림</span>
			<input type="checkbox" bind:checked={notifications} class="accent-primary-500" />
		</label>
	</section>

	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="mb-4 font-semibold">채팅</h2>
		<label class="flex items-center justify-between text-sm">
			<span>중요 대화 자동 기억 저장</span>
			<input type="checkbox" bind:checked={memoryAutoSave} class="accent-primary-500" />
		</label>
	</section>

	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="font-semibold">테마</h2>
		<p class="mt-2 text-sm text-text-muted">다크 모드 (기본)</p>
		<div class="mt-3 flex gap-2">
			<button class="rounded-xl border-2 border-primary-500 bg-bg-primary px-4 py-2 text-sm">다크</button>
			<button class="rounded-xl border border-white/10 px-4 py-2 text-sm text-text-muted" disabled>라이트 (준비 중)</button>
		</div>
	</section>

	<Button variant="ghost" onclick={handleLogout}>로그아웃</Button>
</div>
