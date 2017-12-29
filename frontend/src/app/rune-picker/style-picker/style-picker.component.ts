import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PerksPredictionService } from '../../perks-prediction.service';

@Component({
  selector: 'style-picker',
  templateUrl: './style-picker.component.html',
  styleUrls: ['./style-picker.component.sass']
})
export class StylePickerComponent implements OnInit {

  paths = [
    {id:8000, name:"Precision", color:"#654f3c"},
    {id:8100, name:"Domination", color:"#86454a"},
    {id:8200, name:"Sorcery", color:"#9469e6"},
    {id:8300, name:"Inspiration", color:"#3c5b66"},
    {id:8400, name:"Resolve", color:"#467646"}
  ]

  @Input()
  disabled:number;

  @Input()
  percentages:{[index:number]:number}

  @Output()
  selected = new EventEmitter<number>();

  highest:number;
  selectedPath:number;

  constructor(private perksService:PerksPredictionService) { }

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

  changeSelected(selected){
    this.selectedPath = selected;
  }

  continue(){
    this.selected.emit(this.selectedPath);
    this.perksService.setPrimaryPath(this.selectedPath);
  }

}
