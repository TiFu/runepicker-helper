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

}
