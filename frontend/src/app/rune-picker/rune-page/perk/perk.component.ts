import { Component, OnInit, Input } from '@angular/core';
import { StaticDataService } from '../../../static-data/static-data.service';

@Component({
  selector: 'perk',
  templateUrl: './perk.component.html',
  styleUrls: ['../shared.sass','./perk.component.sass']
})
export class PerkComponent implements OnInit {

  @Input() perk:number;
  @Input() keystone:boolean = false;
  @Input() path:number;

  constructor(private staticData:StaticDataService) { }

  ngOnInit() {
  }

  getName(){
    if(this.perk){
      return this.staticData.perksDescription[this.perk].name
    }
  }

  getColor(){
    if(this.path){
      return this.staticData.paths[this.path].color;
    }
  }

  getShortDescription(){
    if(this.perk){
      return this.staticData.perksDescription[this.perk].shortDesc
    }
  }

}
