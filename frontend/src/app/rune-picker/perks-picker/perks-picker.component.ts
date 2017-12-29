import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PerksPredictionService } from '../../perks-prediction.service';

@Component({
  selector: 'perks-picker',
  templateUrl: './perks-picker.component.html',
  styleUrls: ['./perks-picker.component.sass']
})
export class PerksPickerComponent implements OnInit {

  @Input()
  perks;

  @Output()
  selected = new EventEmitter<number[]>();

  selectedPerks:number[] = [];

  constructor(private perksService:PerksPredictionService) { }

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

}
