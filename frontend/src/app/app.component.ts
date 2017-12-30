declare let navigator:any;

import { Component } from '@angular/core';
import { LcuConnectorService } from "./lcu-connector/lcu-connector.service";
import { PerksPredictionService } from "./perks-prediction.service";
import { environment } from "../environments/environment"

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {

  socketConnected = false;
  environment = environment;
  constructor(public lcu:LcuConnectorService, private perks:PerksPredictionService){

  }

  ngOnInit(){
    console.log("LCU Availiability", this.lcu.isAvailable())
    this.perks.socketConnected.subscribe((connected)=>{
      this.socketConnected = connected
    });
  }
}
