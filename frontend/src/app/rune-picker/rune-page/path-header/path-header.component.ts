import { Component, OnInit, Input } from '@angular/core';
import { StaticDataService } from '../../../static-data/static-data.service';

@Component({
  selector: 'path-header',
  templateUrl: './path-header.component.html',
  styleUrls: ['./path-header.component.sass', '../shared.sass']
})
export class PathHeaderComponent implements OnInit {

  @Input() path:number;
  random = Math.random()

  constructor(private staticData: StaticDataService) { }

  ngOnInit() {

  }


  color(){
    if(this.path){
      return this.staticData.paths[this.path].color;
    }else{
      return "black"
    }
  }

  getName():string{
    if(this.path){
      return this.staticData.paths[this.path].name;
    }
  }

  getDescription():string{
    if(this.path){
      return this.staticData.paths[this.path].tooltip;
    }
  }

}
