declare function require(url: string);

import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';
let champMap = require("./champions.json")

@Component({
  selector: 'champion-selection',
  templateUrl: './champion-selection.component.html',
  styleUrls: ['./champion-selection.component.css']
})
export class ChampionSelectionComponent implements OnInit {

  @Output()
  championSelected:EventEmitter<any> = new EventEmitter<any>()

  champList:any = [];
  champMap = champMap;
  constructor(private sanitizer:DomSanitizer) { }

  ngOnInit() {
    this.champList = Object.keys(champMap)
  }

  championClicked(champ){
    this.championSelected.emit(champMap[champ])
  }

}
