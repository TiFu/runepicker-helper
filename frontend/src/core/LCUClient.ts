export interface Page {
    id: number;
    
}

export interface LCUClient {

    /**
     * Signals if the lcu client is available in the current
     * **distribution** i.e. false in web, true in electron
     */
    isAvailable(): boolean;
    getPages(): Promise<Array<Page>>;
    getMaxPages(): Promise<number>;
    createPage(page: Page): Promise<Page>;
    deletePage(pageId: number): Promise<void>;
    selectPage(pageId: number): Promise<void>;
}