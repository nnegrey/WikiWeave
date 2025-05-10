import React from 'react';
import { Box, Paper, Typography, Divider } from '@mui/material';
import { WikiPath } from '../types/wiki';

interface StoryDisplayProps {
    path: WikiPath;
}

const StoryDisplay: React.FC<StoryDisplayProps> = ({ path }) => {
    return (
        <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
                From: {path.start_page.title}
            </Typography>
            <Typography variant="h5" gutterBottom>
                To: {path.end_page.title}
            </Typography>

            <Divider sx={{ my: 2 }} />

            <Typography variant="h6" gutterBottom>
                Path:
            </Typography>

            {path.path.map((page, index) => (
                <Box key={page.id} sx={{ mb: 2 }}>
                    <Typography variant="subtitle1">
                        {index + 1}. {page.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {page.summary}
                    </Typography>
                </Box>
            ))}
        </Paper>
    );
};

export default StoryDisplay;
