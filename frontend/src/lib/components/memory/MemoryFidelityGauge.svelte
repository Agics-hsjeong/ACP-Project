<script lang="ts">
	interface Props {
		value: number;
		label?: string;
	}

	let { value, label = '기억 충실도' }: Props = $props();
</script>

<div>
	<div class="mb-3 flex items-center justify-between">
		<h3 class="text-sm font-semibold">{label}</h3>
		<span class="text-2xl font-bold text-primary-300">{value}%</span>
	</div>
	<div class="h-3 overflow-hidden rounded-full bg-bg-primary/80">
		<div
			class="h-full rounded-full bg-gradient-to-r from-primary-600 to-accent-green transition-all duration-700"
			style="width: {value}%"
		></div>
	</div>
	<p class="mt-2 text-xs text-text-muted">AI가 대화 맥락을 얼마나 정확히 기억하는지 나타냅니다.</p>
</div>
