export interface PageNode {
    id: number;
    title: string;
    summary: string;
    embedding: number[];
}

export interface WikiPath {
    start_page: PageNode;
    end_page: PageNode;
    path: PageNode[];
}
