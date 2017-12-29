declare function require(url: string);

import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'champion-list',
  templateUrl: './champion-list.component.html',
  styleUrls: ['./champion-list.component.sass']
})
export class ChampionListComponent implements OnInit {

  @Output()
  championChanged:EventEmitter<any> = new EventEmitter<any>()

  champList:any = [];
  champMap = require("./champions.json");
  constructor() { }

  ngOnInit() {
    this.champList = Object.keys(this.champMap)
  }

  championClicked(champ){
    this.championChanged.emit(this.champMap[champ])
  }

}
