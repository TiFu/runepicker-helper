declare function require(url: string);
declare var Buffer:any;
declare var electron: any;
declare var LCUConnector:any;
import {LCUClient, Page} from './LCUClient';
import * as request from 'request'


export class LCUClientImpl implements LCUClient {
    private url: string;
    private port: number;
    private password: string;
    private protocol: string;
    private username: string = "riot";

    private connected: boolean = false;
    private connector: any;

    constructor(onLCUConnectListener: () => void, onLCUDisconnectListener: () => void) {
        this.connector = new LCUConnector();
        this.connector.on("connect", (data: any) => {
            this.url = data.address;
            this.port = data.port;
            this.password = data.password;
            this.protocol = data.protocol;
            this.username = data.username;
            this.connected = true;
            onLCUConnectListener();
        })
        this.connector.on("disconnect", (data: any) => {
            this.connected = false;
            onLCUDisconnectListener();
        });
        this.connector.start();
    }

    public disconnect(): void {
        this.connector.stop();
    }

    public isConnected(): boolean {
        return this.connected;
    }

    private getKey(): string {
        return new Buffer(this.username + ":" + this.password).toString("base64");
    }

    isAvailable(): boolean {
        return true;
    }

    getPages(): Promise<Page[]> {
       return this.requestPromise(this.getOptions("GET", "/lol-perks/v1/pages"));
    }

    private getOptions(method: string, path: string, data: any = null) {
        let options = {
            method: method,
            uri: this.protocol + "://" + this.url + ":" + this.port + path,
            headers: {
               "Authorization": "Basic " + this.getKey()
            },
            json: data || true,
            agentOptions: {
                host: this.url,
                port: this.port,
                path: path,
                rejectUnauthorized: false
            }
       }
       return options;
    }

    private requestPromise(options: any): Promise<any> {
        return new Promise((resolve, reject) => {
            request(options.uri, options, (error: any, response: any, body: any) => {
                if (error != null) {
                    console.log(error)
                    reject(error);
                    return;
                }
                console.log(options.uri + " [" + options.method + "]" + ": " + response.statusCode)
                if (response.statusCode >= 200 && response.statusCode < 300) {
                    resolve(body);
                } else {
                    reject(response.body);
                }
            })
        });
    }

    getMaxPages(): Promise<number> {
        return this.requestPromise(this.getOptions("GET", "/lol-perks/v1/inventory")).then((body: any) => body.ownedPageCount);
    }

    createPage(page: Page): Promise<Page> {
        return this.requestPromise(this.getOptions("POST", "/lol-perks/v1/pages/",  page));
    }

    deletePage(pageId: number): Promise<void> {
        return this.requestPromise(this.getOptions("DELETE", "/lol-perks/v1/pages/" + pageId));
    }

    selectPage(pageId: number): Promise<void> {
        return this.requestPromise(this.getOptions("PUT", "/lol-perks/v1/currentpage", pageId));
    }

}
