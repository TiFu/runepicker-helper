declare function require(url: string);

import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { LCUClient, Page } from './LCUClient';
import { Observable } from 'rxjs';
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

  getPages(): Observable<Page[]> {
      return Observable.fromPromise(this.connector.getPages());
  }
  getMaxPages(): Observable<number> {
      return Observable.fromPromise(this.connector.getMaxPages());
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
  replacePage(oldPageId: number, newPage:Page){
    return this.deletePage(oldPageId).then(()=>{
      return this.createPage(newPage);
    }).then((page) => {
      return this.selectPage(page.id).then(()=>page)
    });
  }

}
