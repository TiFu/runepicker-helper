declare function require(url: string);

import { Injectable } from '@angular/core';

@Injectable()
export class StaticDataService {

  champions = require("./champions.json");
  perksDescription = {};
  perksToPath = {}
  paths = {};
  pathsArray;
  keystones = []

  constructor() {
    this.pathsArray = require("./paths.json");
    for(let path of this.pathsArray){
      this.paths[path["id"]] = path;
      for(let perk of path.slots[0].perks){
        this.keystones.push(parseInt(perk))
      }
      for(let i = 0; i < path.slots.length; i++){
        for(let perk of path.slots[i].perks){
          this.perksToPath[perk] = path["id"]
        }
      }
    }
    let tmpDesc = require("./perksDescription.json");
    for(let perk of tmpDesc){
      this.perksDescription[perk["id"]] = perk;
    }
  }

  isKeystone(id):boolean{
    // I have no clue why this is nessesary
    id = parseInt(String(id));
    return this.keystones.includes(id);
  }

}
