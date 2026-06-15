/** 메시지 추가·스트리밍 시 채팅 영역을 하단으로 스크롤 */
export function autoscroll(node: HTMLElement) {
	const scroll = () => {
		node.scrollTop = node.scrollHeight;
	};

	const observer = new MutationObserver(scroll);
	observer.observe(node, { childList: true, subtree: true, characterData: true });
	scroll();

	return {
		destroy() {
			observer.disconnect();
		}
	};
}
