import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { StaticDataService } from '../../static-data/static-data.service';
import {LcuConnectorService} from '../../lcu-connector/lcu-connector.service';

@Component({
  selector: 'rune-page',
  templateUrl: './rune-page.component.html',
  styleUrls: ['./rune-page.component.sass', './shared.sass']
})
export class RunePageComponent implements OnInit {

  @Input() primaryStyle:number;
  @Input() secondaryStyle:number;
  @Input() primaryRunes:number[];
  @Input() secondaryRunes:number[];

  @Output() reset = new EventEmitter<boolean>();

  overlayVisible = false;

  constructor(private staticData:StaticDataService, public lcu:LcuConnectorService) { }

  ngOnInit() {
  }

  getBackground():string{
    return "url(assets/backgrounds/" + this.primaryStyle + ".jpg)";
  }

  getPrimaryColor(){
    if(this.primaryStyle){
      return this.staticData.paths[this.primaryStyle].color;
    }
  }

  counter(i:number){
    return new Array(i);
  }

  get(array, index){
    if(array && array.length > index){
      return array[index];
    }else{
      return null;
    }
  }

  resetClicked(){
    this.reset.emit(true);
  }

  setOverlayOpen(open:boolean){
    this.overlayVisible = open;
  }
}
