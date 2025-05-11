export interface PageNode {
    id: number;
    title: string;
    summary: string;
}

export interface WikiPath {
    start_page: PageNode;
    end_page: PageNode;
    path: PageNode[];
}

export interface WikiNode {
    id: number;
    title: string;
    summary: string;
}

export interface WovenStory {
    nodes: WikiNode[];
    story?: {
        content: string;
    };
}
