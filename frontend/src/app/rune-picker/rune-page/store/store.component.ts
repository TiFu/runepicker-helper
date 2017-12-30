import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { LcuConnectorService } from '../../../lcu-connector/lcu-connector.service';
import { StaticDataService } from '../../../static-data/static-data.service'

@Component({
  selector: 'rune-store',
  templateUrl: './store.component.html',
  styleUrls: ['./store.component.sass']
})
export class StoreComponent implements OnInit {

  @Output() closed = new EventEmitter<boolean>();

  @Input() primaryStyle:number;
  @Input() secondaryStyle:number;
  @Input() primaryRunes:number[];
  @Input() secondaryRunes:number[];

  pageName = "";

  runePages;
  maxPages;
  constructor(private lcu:LcuConnectorService, private staticData:StaticDataService) { }

  ngOnInit() {
    this.update();
  }

  update(){
    this.lcu.getPages().subscribe((pages)=>{
      this.runePages = pages;
      console.log(pages);
    });
    this.lcu.getMaxPages().subscribe((max)=>{
      this.maxPages = max
      console.log(max);
    });
  }

  closeOverlay(){
    this.closed.emit(true);
  }

  getColor(path){
    return this.staticData.paths[path].color;
  }

  addPage(){
    let page = {
      name: this.pageName,
      primaryStyleId: this.primaryStyle,
      subStyleId: this.secondaryStyle,
      selectedPerkIds: this.primaryRunes.concat(this.secondaryRunes)
    }
    this.lcu.createPage(page).then(() => this.update());
  }

  replacePage(name, id){
    let page = {
      name: name,
      primaryStyleId: this.primaryStyle,
      subStyleId: this.secondaryStyle,
      selectedPerkIds: this.primaryRunes.concat(this.secondaryRunes)
    }
    this.lcu.replacePage(id, page).then(() => this.update());
  }

  deletePage(id){
    this.lcu.deletePage(id).then(() => this.update());
  }

  hasEmptyPages(){
    return this.runePages.length - 5 < this.maxPages;
  }
}
