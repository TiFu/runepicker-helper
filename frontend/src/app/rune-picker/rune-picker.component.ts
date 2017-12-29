import { Component, OnInit } from '@angular/core';
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
  }

  selected(event){
    this.lane = event.lane;
    this.champ = event.champ;
    this.perksService.startPrediction(this.champ.id, this.lane);
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
}

abstract class State{
  constructor(protected perksService:PerksPredictionService,protected store:Store){ }
  abstract handleStateChange(type:string, data:any): State;
  abstract getId():number;

  pathSelected(path:number){}
  runesSelected(runes:number[]){}
  getSuggestedStyles(){return {}}
  getSuggestedRunes() {return []}
}


class ChampionSelectState extends State{
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
}

class SecondaryPageSelectState extends State{
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
  handleStateChange(type:string, data:any):State{
    return this;
  }
  getSuggestedRunes(){
    return this.store.suggestedSecondaryRunes;
  }
  getId(){return 2;}
}
