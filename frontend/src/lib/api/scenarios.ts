import { apiFetch } from './client';

export type CharacterScenario = {
	character_id: string;
	scenario_id: string;
	title: string;
	description: string;
	prompt: string;
	is_default: boolean;
	created_at: string;
	updated_at: string;
};

export async function fetchCharacterScenarios(characterId: string): Promise<CharacterScenario[]> {
	return apiFetch<CharacterScenario[]>(`/characters/${characterId}/scenarios/`);
}

