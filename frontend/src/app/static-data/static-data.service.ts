declare function require(url: string);

import { Injectable } from '@angular/core';

@Injectable()
export class StaticDataService {

  champions = require("./champions.json");
  perksDescription = {};
  paths = {};

  constructor() {
    let tmpPaths = require("./paths.json");
    for(let path of tmpPaths){
      this.paths[path["id"]] = path;
    }
    let tmpPerks = require("./perksDescription.json");
    for(let perk of tmpPerks){
      this.perksDescription[perk["id"]] = perk;
    }
  }

}
