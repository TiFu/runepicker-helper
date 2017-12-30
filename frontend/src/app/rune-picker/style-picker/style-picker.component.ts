import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PerksPredictionService } from '../../perks-prediction.service';
import { StaticDataService } from '../../static-data/static-data.service';

@Component({
  selector: 'style-picker',
  templateUrl: './style-picker.component.html',
  styleUrls: ['./style-picker.component.sass']
})
export class StylePickerComponent implements OnInit {

  @Input()  disabled:number;

  @Input()  percentages:{[index:number]:number}

  @Input() title:string;

  @Output()
  selected = new EventEmitter<number>();


  highest:number;
  selectedPath:number;

  constructor(private perksService:PerksPredictionService, public staticData:StaticDataService) { }

  ngOnInit() {
    let max = -1;
    for(let key in this.percentages){
      if(max == -1 || this.percentages[key] > this.percentages[max]){
        max = parseInt(key);
      }
    }
    this.highest = max;
    this.selectedPath = max;
  }

  getPercentage(id){
    if(!this.percentages[id]){
      return "primary";
    }
    return Math.round(this.percentages[id] * 100 * 100) / 100
  }

  getRecommendedPath(){
    return this.staticData.paths[this.highest];
  }

  getPickedPath(){
    return this.staticData.paths[this.selectedPath];
  }

  changeSelected(selected){
    this.selectedPath = selected;
  }

  continue(){
    this.selected.emit(this.selectedPath);
    this.perksService.setPrimaryPath(this.selectedPath);
  }

}
