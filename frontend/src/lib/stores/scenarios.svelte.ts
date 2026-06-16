import { apiHealth } from '$lib/api/client';
import { fetchCharacterScenarios, type CharacterScenario } from '$lib/api/scenarios';

let byCharacter = $state<Record<string, CharacterScenario[]>>({});

export async function initScenarios(characterId: string) {
	if (!(await apiHealth())) return;
	if (byCharacter[characterId]) return;
	try {
		byCharacter[characterId] = await fetchCharacterScenarios(characterId);
	} catch (err) {
		console.error('Scenarios load failed:', err);
		byCharacter[characterId] = [];
	}
}

export function getCharacterScenarios(characterId: string): CharacterScenario[] {
	return byCharacter[characterId] ?? [];
}

