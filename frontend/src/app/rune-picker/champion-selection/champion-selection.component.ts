import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'champion-selection',
  templateUrl: './champion-selection.component.html',
  styleUrls: ['./champion-selection.component.sass']
})
export class ChampionSelectionComponent implements OnInit {

  overlayShown:boolean = false;
  lane:string = null;
  champ:any = null;

  @Output()
  selected = new EventEmitter<{lane:string, champ:any}>();

  constructor() { }

  ngOnInit() {
  }

  getChampionImageUrl():string{
    if(!this.champ){
      return "assets/champions/-1.png";
    }else{
      return "assets/champions/" + this.champ.id + ".png";
    }

  }

  start(){
    if(this.lane && this.champ){
      this.selected.emit({lane:this.lane, champ:this.champ})
    }
  }

  toggleChampionSelection(){
    this.overlayShown = !this.overlayShown
  }

  laneChanged(lane){
    this.lane = lane;
  }

  championChanged(champ){
    this.champ = champ;
    this.overlayShown = false;
  }

}
