import { LCUClient, Page } from './LCUClient';

export class LCUClientImpl implements LCUClient{
  isConnected(): boolean {
        return false;
    }

    disconnect(): void {

    }

    isAvailable(): boolean {
        return false;
    }

    getPages(): Promise<Page[]> {
        throw new Error("Method not implemented.");
    }
    getMaxPages(): Promise<number> {
        throw new Error("Method not implemented.");
    }
    createPage(page: Page): Promise<Page> {
        throw new Error("Method not implemented.");
    }
    deletePage(pageId: number): Promise<void> {
        throw new Error("Method not implemented.");
    }
    selectPage(pageId: number): Promise<void> {
        throw new Error("Method not implemented.");
    }
}
