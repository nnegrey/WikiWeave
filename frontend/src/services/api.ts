import axios from 'axios';
import { WikiPath, WovenStory } from '../types/wiki';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const api = {
    getRandomPath: async (): Promise<WikiPath> => {
        const response = await axios.get(`${API_BASE_URL}/random-path`);
        return response.data;
    },
    getWovenStory: async (): Promise<WovenStory> => {
        const response = await axios.get(`${API_BASE_URL}/woven-story`);
        return response.data;
    },
};
