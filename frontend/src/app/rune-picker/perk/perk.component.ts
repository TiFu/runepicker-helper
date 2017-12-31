import { Component, OnInit, Input } from '@angular/core';
import { StaticDataService } from '../../static-data/static-data.service';

@Component({
  selector: 'perk',
  templateUrl: './perk.component.html',
  styleUrls: ['./perk.component.sass']
})
export class PerkComponent implements OnInit {

  KEYSTONES:number[];

  @Input() perk:number;
  keystone:boolean;

  constructor(private staticData:StaticDataService) { }

  ngOnInit() {
    this.keystone = this.staticData.isKeystone(this.perk);
  }

  getTooltip() {
    let tooltip = "<span class=\"big\"><b>" + this.getName() + "</b></span></br>&nbsp;</br>";
    tooltip += this.getDescription();
    return tooltip;
  }
  getName() {
    if (this.perk) {
      return this.staticData.perksDescription[this.perk].name;
    }
  }
  
  getDescription(){
    if(this.perk){
      return this.staticData.perksDescription[this.perk].longDesc;
    }
  }

  getColor(){
    if(this.perk){
      let path = this.staticData.perksToPath[this.perk];
      return this.staticData.paths[path].color;
    }
  }

}
