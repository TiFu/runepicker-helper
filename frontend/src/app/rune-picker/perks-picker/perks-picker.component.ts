import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PerksPredictionService } from '../../perks-prediction.service';
import { StaticDataService } from '../../static-data/static-data.service';

@Component({
  selector: 'perks-picker',
  templateUrl: './perks-picker.component.html',
  styleUrls: ['./perks-picker.component.sass']
})
export class PerksPickerComponent implements OnInit {

  @Input()
  perks;

  @Input()
  path;

  @Output()
  selected = new EventEmitter<number[]>();

  selectedPerks:number[] = [];

  constructor(private perksService:PerksPredictionService, private staticData:StaticDataService) { }

  ngOnInit() {
    console.log(this.perks);
    for (let row of this.perks){
      this.selectedPerks.push(this.getMax(row));
    }
  }

  keys(map){
    return Object.keys(map);
  }

  getMax(row){
    let max = -1;
    for(let key of this.keys(row)){
      if(max == -1 || row[key] > row[max]){
        max = parseInt(key);
      }
    }
    return max;
  }

  continue(){
    this.selected.emit(this.selectedPerks);
  }

  getRowTitle(index:number){
    let title = "";
    if(this.isPrimaryPath()){
      switch(index){
        case 0: title =  "Keystone"; break;
        case 1: title =  "Greater Rune"; break;
        case 2: title =  "Lesser Runes"; break;
      }
    }else{
      if(index == 0){
        title = "Lesser Runes";
      }
    }
    return title;
  }

  isPrimaryPath(){
    return this.perks.length > 2
  }

  getColor(){
    return this.staticData.paths[this.path].color;
  }

}
