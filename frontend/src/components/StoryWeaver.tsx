import React, { useState } from 'react';
import { Button, CircularProgress, Box, FormControlLabel, Switch, Typography, Paper } from '@mui/material';
import { api } from '../services/api';
import { WovenStory, WikiPath } from '../types/wiki';
import StoryDisplayer from './StoryDisplayer';

const StoryWeaver: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [story, setStory] = useState<WovenStory | WikiPath | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [includeStory, setIncludeStory] = useState(true);

    const handleWeaveStory = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = includeStory
                ? await api.getWovenStory()
                : await api.getRandomPath();
            setStory(result);
        } catch (err) {
            setError('Failed to weave story. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h6" gutterBottom>
                        Choose Generation Mode
                    </Typography>
                    <FormControlLabel
                        control={
                            <Switch
                                checked={includeStory}
                                onChange={(e) => setIncludeStory(e.target.checked)}
                                color="primary"
                                size="medium"
                            />
                        }
                        label={
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                {includeStory ? 'Links & Woven Story' : 'Path Only'}
                            </Typography>
                        }
                        sx={{ mb: 3 }}
                    />
                    <Button
                        variant="contained"
                        color="primary"
                        size="large"
                        onClick={handleWeaveStory}
                        disabled={loading}
                        sx={{ minWidth: 200 }}
                    >
                        {loading ? <CircularProgress size={24} /> : 'Generate'}
                    </Button>
                </Box>
            </Paper>

            {error && (
                <Box sx={{ color: 'error.main', textAlign: 'center', mb: 2 }}>
                    {error}
                </Box>
            )}

            {story && <StoryDisplayer story={story} />}
        </Box>
    );
};

export default StoryWeaver;
