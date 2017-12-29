import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'lane-select-wheel',
  templateUrl: './wheel.component.html',
  styleUrls: ['./wheel.component.css']
})
export class LaneSelectWheelComponent implements OnInit {

  @Output()
  change: EventEmitter<string> = new EventEmitter<string>();

  constructor() { }

  ngOnInit() {
  }

  imageClicked(string){
    this.change.emit(string)
  }

}
