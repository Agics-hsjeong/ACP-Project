<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
</script>

<svelte:head>
	<title>설정 — ACP</title>
</svelte:head>

<div class="mx-auto max-w-lg space-y-6">
	<h1 class="text-2xl font-bold">설정</h1>
	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="font-semibold">계정</h2>
		<p class="mt-2 text-sm text-text-muted">이메일, 비밀번호, 연동 계정 관리 (API 연동 예정)</p>
	</section>
	<section class="rounded-2xl border border-white/10 bg-bg-surface/50 p-6">
		<h2 class="font-semibold">테마</h2>
		<p class="mt-2 text-sm text-text-muted">다크 모드 (기본) · 라이트 모드 Phase 1+</p>
	</section>
	<Button href="/login" variant="ghost">로그아웃</Button>
</div>
