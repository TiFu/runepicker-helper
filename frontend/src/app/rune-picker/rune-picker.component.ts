import { Component, OnInit } from '@angular/core';
import { PerksPredictionAPIListener, PerksPredictionAPI, Response, PerkPrediction, PerkStylePrediction} from '../core/PerksPredictionAPI'

@Component({
  selector: 'app-rune-picker',
  templateUrl: './rune-picker.component.html',
  styleUrls: ['./rune-picker.component.sass']
})
export class RunePickerComponent implements OnInit {

  lane:string = null;
  champ:any = null;
  state = 0;
  perksApi:PerksPredictionAPI;

  constructor() { }

  ngOnInit() {
    //TODO: move this to a service
    this.perksApi = new PerksPredictionAPI("localhost:8765");
    this.perksApi.connect(new PerksPredictionListener())
    this.perksApi.startPrediction({championId:1,lane:"MIDDLE"})
  }

  selected(event){
    console.log(event);
    this.lane = event.lane;
    this.champ = event.champ;
    this.state = 1;
  }

}

class PerksPredictionListener implements PerksPredictionAPIListener{
  onConnect():void{
    console.log("Hello World")
  }

  onDisconnect():void{

  }

  onReceivedPrimaryStyle(predictions: Response<PerkStylePrediction>): void{
    console.log(predictions)
  }
  onReceivedSubStyle(predictions: Response<PerkStylePrediction>): void{

  }
  onReceivedPrimaryPerks(prediction: Response<PerkPrediction>): void{

  }
  onReceivedSubPerks(prediction:  Response<PerkPrediction>): void{

  }

}
