import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'lane-select',
  templateUrl: './lane-select.component.html',
  styleUrls: ['./lane-select.component.css']
})
export class LaneSelectComponent implements OnInit {

  lane:string = "none";
  laneSelectVisible:boolean = false;

  @Input() disabled:boolean = false;

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

  getLaneSelectBorder(){
    if(this.disabled){
      return "assets/various/lane-select-disabled.png";
    }else{
      return "assets/various/lane-select.png";
    }
  }

  getLaneIcon(){
    if(this.disabled){
      return "assets/lane/none-disabled.png"
    }else{
      return "assets/lane/" + this.lane + ".png";
    }
  }

}
