import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PerksPredictionService } from '../../perks-prediction.service';
import { StaticDataService } from '../../static-data/static-data.service';

@Component({
  selector: 'subperks-picker',
  templateUrl: './subperks-picker.component.html',
  styleUrls: ['./subperks-picker.component.sass']
})
export class SubperksPickerComponent implements OnInit {

  @Input()
  perks;
  
  @Input()
  path;

  @Input()
  title;
  
  @Output()
  selected = new EventEmitter<number[]>();

  selectableRunes: Array<Array<number>>
  perk1: number;
  perk2: number;
  
  predictedPerk1: number;
  predictedPerk2: number;

  nextRuneMoved = 1;

  constructor(private perksService:PerksPredictionService, private staticData:StaticDataService) { }

  ngOnInit() {
    console.log(this.perks);
    // read runes 
    this.selectableRunes = []
    for (let i = 1; i < 4; i++) {
      let perks = this.staticData.paths[this.path]["slots"][i]["perks"];
      this.selectableRunes.push(perks)      
    }
    this.setInitialPerks();
  }

  selectRune(rowId, runeId) {
    if (runeId == this.perk1 || runeId == this.perk2) {
      return;
    }

    // if we have a rune in that row, update that rune
    if (this.selectableRunes[rowId].indexOf(this.perk1) !== -1) {
      this.perk1 = runeId;
      this.nextRuneMoved = 2;
      return;
    } else if (this.selectableRunes[rowId].indexOf(this.perk2) !== -1) {
      this.perk2 = runeId;
      this.nextRuneMoved = 1;
      return;
    }

    // we now KNOW that we are in a row without another rune => move the next one here
    if (this.nextRuneMoved == 1) {
      this.nextRuneMoved = 2;
      this.perk1 = runeId;
    } else if (this.nextRuneMoved == 2) {
      this.nextRuneMoved = 1;
      this.perk2 = runeId;
    }
  }

  setInitialPerks() {
    // find the max for the first one
    this.perk1 = this.getMax(this.perks[0])
    this.predictedPerk1 = this.perk1;
    console.log("FIRST PERK:" + this.perk1);
    // find row of perk 1
    let rowId = this.getRowIdForFirstPerk();  
    console.log("Exclude:" + this.selectableRunes[rowId])
    this.perk2 = this.getMax(this.perks[1], this.selectableRunes[rowId])
    console.log("SECOND PERK: " + this.perk2)
    this.predictedPerk2 = this.perk2;
  }

  getRowIdForFirstPerk(): number {
    let rowId = 0;
    for (let i = 0; i < this.selectableRunes.length; i++) {
      let set = this.selectableRunes[i];
      if (set.indexOf(this.perk1) !== -1) {
        return i;
      }
    }
  }

  keys(map){
    return Object.keys(map);
  }

  getMax(row, except = new Array()){
    let max = -1;
    console.log("Not: " + except)
    for(let key of this.keys(row)){
      if(except.indexOf(parseInt(key)) === -1 && (max == -1 || row[key] > row[max])) {
        max = parseInt(key);
      }
    }
    return max;
  }

  continue(){
    this.selected.emit([this.perk1, this.perk2].sort());
  }


  getColor(){
    return this.staticData.paths[this.path].color;
  }

}
 