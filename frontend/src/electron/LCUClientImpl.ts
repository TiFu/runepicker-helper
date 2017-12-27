import {Page, LCUClient} from '../core/LCUClient'
const LCUConnector = require('lcu-connector');

class LCUClientImpl implements LCUClient {

    constructor(private url: string, private port: number, private password: string, 
                private protocol: string, private username: string = "riot") {
    }

    isAvailable(): boolean {
        return true;
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