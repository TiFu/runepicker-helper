declare let navigator:any;

import { Component } from '@angular/core';
import { LcuConnectorService } from "./lcu-connector/lcu-connector.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private lcu:LcuConnectorService){

  }

  ngOnInit(){
    console.log("LCU Availiability", this.lcu.isAvailable())
  }
}
