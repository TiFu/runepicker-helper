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
    this.champList = this.champList.sort((a, b) => {
      // because edge cases are fun
      a = a == "MonkeyKing" ? "Wukong" : a;
      b = b == "MonkeyKing" ? "Wukong" : b;
      if (a < b) {
        return -1;
      } else if (a > b) {
        return 1;
      } else {
        return 0;
      }
    })
  }

  championClicked(champ){
    this.championChanged.emit(this.champMap[champ])
  }

}
