import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'champion-select',
  templateUrl: './champion-select.component.html',
  styleUrls: ['./champion-select.component.css']
})
export class ChampionSelectComponent implements OnInit {

  champ:any = null;
  lane:any = null;
  overlayVisible = false;

  constructor() { }

  ngOnInit() {
  }

  toggleChampionSelection(){
    this.overlayVisible = !this.overlayVisible
  }

  champSelected(champ){
    this.champ = champ;
    this.overlayVisible = false;
  }

  laneSelected(lane){
    this.lane = lane;
    console.log(lane)
  }

}
