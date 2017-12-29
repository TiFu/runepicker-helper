import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'lane-select',
  templateUrl: './lane-select.component.html',
  styleUrls: ['./lane-select.component.css']
})
export class LaneSelectComponent implements OnInit {

  lane:string = "none";
  laneSelectVisible:boolean = false;
  
  @Output()
  laneChanged = new EventEmitter<string>();

  constructor() { }

  ngOnInit() {
  }

  laneChangedCallback(lane){
    this.lane = lane;
    this.laneSelectVisible = false;
    this.laneChanged.emit(lane)
  }

}
