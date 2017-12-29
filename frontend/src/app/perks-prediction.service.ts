import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

import * as io from 'socket.io-client';

@Injectable()
export class PerksPredictionService {

  private url = 'http://93.196.59.39:8765/runeprediction'
  private socket;

  socketConnected = new BehaviorSubject<boolean>(false);

  constructor() {
    this.socket = io(this.url);
    this.socket.on('connect', ()=> this.socketConnected.next(true));
    this.socket.on('disconnect', ()=>this.socketConnected.next(false));
  }

  error(sucess, msg){
    console.log(sucess, msg);
  }

  startPrediction(championId:number, lane:string){
    this.socket.emit("startPrediction", {"champion_id":championId, "lane":lane.toUpperCase()}, this.error)

  }

  setPrimaryPath(id:number){
    this.socket.emit("selectPrimaryStyle", id, this.error)
  }

  setPrimaryRunes(runes:number[]){
    this.socket.emit("selectPrimaryRunes", runes, this.error);
  }

  setSecondaryPath(id:number){
    this.socket.emit("selectSubStyle", id, this.error);
  }

  getStateChange(): Observable<any>{
    return new Observable(observer => {
      this.socket.on("primaryStyles", data => {
        observer.next({type:"primaryStyles", data:data.data});
      });
      this.socket.on("primaryRunes", data => {
        observer.next({type:"primaryRunes", data:data.data})
      });
      this.socket.on("subStyles", data => {
        observer.next({type:"subStyles", data:data.data})
      });
      this.socket.on("subRunes", data => {
        observer.next({type:"subRunes", data:data.data})
        this.socket.close();
      })
    });
  }

}
