import {Page, LCUClient} from '../core/LCUClient'
import * as rp from 'request-promise'


const LCUConnector = require('lcu-connector');

class LCUClientImpl implements LCUClient {

    constructor(private url: string, private port: number, private password: string, 
                private protocol: string, private username: string = "riot") {
    }

    private getKey(): string {
        return "";
    }

    isAvailable(): boolean {
        return true;
    }
    
    getPages(): Promise<Page[]> {
       let options = {
           uri: this.url + ":" + this.port + "/lol-perks/v1/pages",
           headers: {
               "Authentication": "Basic " + this.getKey()
           },
           json: true
       }

       return rp(options.uri, options).then((body: any) => {
            return body;
       })

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