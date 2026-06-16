let globalQuery = $state('');

export function getSearchQuery(): string {
	return globalQuery;
}

export function setSearchQuery(value: string) {
	globalQuery = value;
}

export function clearSearchQuery() {
	globalQuery = '';
}
