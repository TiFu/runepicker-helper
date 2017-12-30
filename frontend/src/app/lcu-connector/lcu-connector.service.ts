declare function require(url: string);

import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { LCUClient, Page } from './LCUClient';
let LCU;
if(environment.electron){
  LCU = require('./ElectronLCUClient').LCUClientImpl;
}else{
  LCU = require('./WebLCUClient').LCUClientImpl;
}

@Injectable()
export class LcuConnectorService {

  private connector:LCUClient;

  constructor() {
    this.connector = new LCU();
    console.log(this.connector);
  }

  isConnected(): boolean {
      return this.connector.isConnected();
  }

  disconnect(): void {
      this.connector.disconnect();
  }

  isAvailable(): boolean {
      return this.connector.isAvailable();
  }

  getPages(): Promise<Page[]> {
      return this.connector.getPages();
  }
  getMaxPages(): Promise<number> {
      return this.connector.getMaxPages();
  }
  createPage(page: Page): Promise<Page> {
      return this.connector.createPage(page);
  }
  deletePage(pageId: number): Promise<void> {
      return this.connector.deletePage(pageId);
  }
  selectPage(pageId: number): Promise<void> {
     return this.connector.selectPage(pageId);
  }

}
