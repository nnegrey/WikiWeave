import React, { useState } from 'react';
import { Button, CircularProgress, Box } from '@mui/material';
import { api } from '../services/api';
import { WikiPath } from '../types/wiki';
import StoryDisplay from './StoryDisplayer';

const StoryWeaver: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [story, setStory] = useState<WikiPath | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleWeaveStory = async () => {
        setLoading(true);
        setError(null);
        try {
            const path = await api.getRandomPath();
            setStory(path);
        } catch (err) {
            setError('Failed to weave story. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
                <Button
                    variant="contained"
                    color="primary"
                    size="large"
                    onClick={handleWeaveStory}
                    disabled={loading}
                    sx={{ minWidth: 200 }}
                >
                    {loading ? <CircularProgress size={24} /> : 'Weave a Story'}
                </Button>
            </Box>

            {error && (
                <Box sx={{ color: 'error.main', textAlign: 'center', mb: 2 }}>
                    {error}
                </Box>
            )}

            {story && <StoryDisplay path={story} />}
        </Box>
    );
};

export default StoryWeaver;
