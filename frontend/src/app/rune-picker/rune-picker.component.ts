import { Component, OnInit, EventEmitter } from '@angular/core';
import { PerksPredictionService } from '../perks-prediction.service';


@Component({
  selector: 'app-rune-picker',
  templateUrl: './rune-picker.component.html',
  styleUrls: ['./rune-picker.component.sass']
})
export class RunePickerComponent implements OnInit {

  lane:string = null;
  champ:any = null;
  state = null;
  store = new Store();
  primaryStyles:{[index:number]: number}

  constructor(private perksService:PerksPredictionService) { }

  ngOnInit() {
    this.state = new ChampionSelectState(this.perksService, this.store);
    this.perksService.getStateChange().subscribe(message => {
      console.log(message);
      this.state = this.state.handleStateChange(message.type, message.data);
    })
    // This is used for internal state changes without intervention from the service
    this.store.stateChanged.subscribe(message => {
      this.state = this.state.handleStateChange(message.type, message.data);
    });
  }

  selected(event){
    this.lane = event.lane;
    this.champ = event.champ;
    this.perksService.startPrediction(this.champ.id, this.lane);
  }

  reset(){
    this.store.stateChanged.emit({type:"reset",data:{}})
  }

}

class Store{
  primaryStyles:{[index:number]:number}
  primaryStyle:number;
  subStyles:{[index:number]:number}
  subStyle:number;
  suggestedPrimaryRunes:any;
  pickedPrimaryRunes:number[];
  suggestedSecondaryRunes:any;
  pickedSecondaryRunes:any;
  stateChanged = new EventEmitter<any>();
  clear(){
    this.primaryStyles = null;
    this.primaryStyle = null;
    this.subStyles = null;
    this.subStyle = null;
    this.suggestedPrimaryRunes = null;
    this.pickedPrimaryRunes = null;
    this.suggestedSecondaryRunes = null;
    this.pickedSecondaryRunes = null;
  }
}

abstract class State{
  title = "Change it in every State";
  constructor(protected perksService:PerksPredictionService,protected store:Store){ }
  abstract handleStateChange(type:string, data:any): State;
  abstract getId():number;

  pathSelected(path:number){}
  runesSelected(runes:number[]){}
  getSuggestedStyles(){return {}}
  getSuggestedRunes() {return []}
  getTitle(){
    return this.title;
  }
  getStyle(){
    return 0;
  }
}


class ChampionSelectState extends State{
  title = "";
  handleStateChange(type:string, data:any){
    if(type == "primaryStyles"){
      this.store.primaryStyles = data;
      return new PrimaryPageSelectState(this.perksService, this.store);
    }else{
      return this;
    }
  }

  getId():number{
    return 0;
  }
}

class PrimaryPageSelectState extends State{
  "title" = "Primary Path";
  handleStateChange(type:string, data:any):State{
    if(type == "primaryRunes"){
      this.store.suggestedPrimaryRunes = data;
      return new PrimaryPerksSelectState(this.perksService,this.store)
    }
    return this;
  }
  getId():number{return 1;}
  pathSelected(path:number){
    this.store.primaryStyle = path;
    this.perksService.setPrimaryPath(path);
  }
  getSuggestedStyles(){
    return this.store.primaryStyles;
  }
}

class PrimaryPerksSelectState extends State{
  title = "Perks of Primary Path";
  handleStateChange(type:string, data:any):State{
    if(type == "subStyles"){
      this.store.subStyles = data;
      return new SecondaryPageSelectState(this.perksService, this.store);
    }
    return this;
  }
  getId():number{return 2;}
  runesSelected(runes:number[]){
    this.store.pickedPrimaryRunes = runes;
    this.perksService.setPrimaryRunes(runes);
  }
  getSuggestedRunes(){
    return this.store.suggestedPrimaryRunes;
  }
  getStyle(){
    return this.store.primaryStyle;
  }
}

class SecondaryPageSelectState extends State{
  title = "Secondary Path";
  handleStateChange(type:string, data:any):State{
    if(type == "subRunes"){
      this.store.suggestedSecondaryRunes = data;
      return new SecondaryRunesSelectState(this.perksService, this.store);
    }
    return this;
  }
  getId():number{return 1}
  pathSelected(path:number){
    this.store.subStyle = path;
    this.perksService.setSecondaryPath(path);
  }
  getSuggestedStyles(){
    return this.store.subStyles;
  }
}

class SecondaryRunesSelectState extends State{
  title = "Perks of Secondary Path"
  handleStateChange(type:string, data:any):State{
    if(type == "done"){
      return new RunePageDisplayState(this.perksService, this.store);
    }
    return this;
  }
  getSuggestedRunes(){
    return this.store.suggestedSecondaryRunes;
  }
  runesSelected(runes){
    this.store.pickedSecondaryRunes = runes;
    this.store.stateChanged.emit({type:"done",data:{}})
  }
  getId(){return 4;}
  getStyle(){
    return this.store.subStyle;
  }
}

class RunePageDisplayState extends State{
  handleStateChange(type: string, data:any):State{
    if(type == "reset"){
      this.store.clear();
      return new ChampionSelectState(this.perksService, this.store);
    }
    return this;
  }
  getId(){return 3;}
}
