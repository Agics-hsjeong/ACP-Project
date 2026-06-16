export function uuid(): string {
	const c = globalThis.crypto as Crypto | undefined;
	const fn = c?.randomUUID;
	if (typeof fn === 'function') return fn.call(c);

	// Fallback: RFC4122 v4-like (not cryptographically strong)
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (ch) => {
		const r = Math.floor(Math.random() * 16);
		const v = ch === 'x' ? r : (r & 0x3) | 0x8;
		return v.toString(16);
	});
}

