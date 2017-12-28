import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { ChampionSelectComponent } from './champion-select/champion-select.component';
import { LaneSelectComponent } from './champion-select/lane-select/lane-select.component';
import { WheelComponent } from './champion-select/lane-select/wheel/wheel.component';
import { ChampionSelectionComponent } from './champion-select/champion-selection/champion-selection.component';

@NgModule({
  declarations: [
    AppComponent,
    ChampionSelectComponent,
    LaneSelectComponent,
    WheelComponent,
    ChampionSelectionComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
