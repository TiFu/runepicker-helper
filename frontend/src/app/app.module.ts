import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { routing } from './app.router';

import { AppComponent } from './app.component';
import { RunePickerComponent } from './rune-picker/rune-picker.component';
import { ChampionSelectionComponent } from './rune-picker/champion-selection/champion-selection.component';
import { ChampionListComponent } from './rune-picker/champion-selection/champion-list/champion-list.component';
import { LaneSelectComponent } from './rune-picker/champion-selection/lane-select/lane-select.component';
import { LaneSelectWheelComponent } from './rune-picker/champion-selection/lane-select/wheel/wheel.component';

@NgModule({
  declarations: [
    AppComponent,
    RunePickerComponent,
    ChampionSelectionComponent,
    ChampionListComponent,
    LaneSelectComponent,
    LaneSelectWheelComponent
  ],
  imports: [
    BrowserModule,
    routing
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
