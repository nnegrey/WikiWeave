import React from 'react';
import { Box, Paper, Typography, Divider } from '@mui/material';
import { WovenStory, WikiPath } from '../types/wiki';

interface StoryDisplayProps {
    story: WovenStory | WikiPath;
}

const StoryDisplayer: React.FC<StoryDisplayProps> = ({ story }) => {
    const nodes = 'nodes' in story ? story.nodes : story.path;
    const hasStory = 'story' in story && story.story?.content;

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
            {/* Path Display */}
            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <Typography variant="h5" gutterBottom>
                    Evolutionary Path
                </Typography>
                <Divider sx={{ my: 2 }} />
                {nodes.map((node, index) => (
                    <Box key={node.id} sx={{ mb: 2 }}>
                        <Typography variant="h6" color="primary">
                            {index + 1}. {node.title}
                        </Typography>
                        <Typography variant="body1" color="text.secondary">
                            {node.summary}
                        </Typography>
                    </Box>
                ))}
            </Paper>

            {/* Story Display */}
            {hasStory && (
                <Paper elevation={3} sx={{ p: 3 }}>
                    <Typography variant="h5" gutterBottom>
                        The Woven Story
                    </Typography>
                    <Divider sx={{ my: 2 }} />
                    <Typography
                        variant="body1"
                        sx={{
                            whiteSpace: 'pre-line',
                            lineHeight: 1.8,
                            '& strong': {
                                color: 'primary.main'
                            }
                        }}
                    >
                        {story.story?.content}
                    </Typography>
                </Paper>
            )}
        </Box>
    );
};

export default StoryDisplayer;
