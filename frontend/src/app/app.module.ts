import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';

import { routing } from './app.router';

import { PerksPredictionService } from './perks-prediction.service';
import { LcuConnectorService } from './lcu-connector/lcu-connector.service';
import { StaticDataService } from './static-data/static-data.service';

import { AppComponent } from './app.component';
import { RunePickerComponent } from './rune-picker/rune-picker.component';
import { ChampionSelectionComponent } from './rune-picker/champion-selection/champion-selection.component';
import { ChampionListComponent } from './rune-picker/champion-selection/champion-list/champion-list.component';
import { LaneSelectComponent } from './rune-picker/champion-selection/lane-select/lane-select.component';
import { LaneSelectWheelComponent } from './rune-picker/champion-selection/lane-select/wheel/wheel.component';
import { StylePickerComponent } from './rune-picker/style-picker/style-picker.component';
import { PerksPickerComponent } from './rune-picker/perks-picker/perks-picker.component';
import { SubperksPickerComponent } from './rune-picker/subperks-picker/subperks-picker.component';
import { RunePageComponent } from './rune-picker/rune-page/rune-page.component';
import { PathHeaderComponent } from './rune-picker/rune-page/path-header/path-header.component';
import { PagePerkComponent } from './rune-picker/rune-page/perk/perk.component';
import { PerkComponent } from './rune-picker/perk/perk.component';
import { StoreComponent } from './rune-picker/rune-page/store/store.component';

@NgModule({
  declarations: [
    AppComponent,
    RunePickerComponent,
    SubperksPickerComponent,
    ChampionSelectionComponent,
    ChampionListComponent,
    LaneSelectComponent,
    LaneSelectWheelComponent,
    StylePickerComponent,
    PerksPickerComponent,
    RunePageComponent,
    PathHeaderComponent,
    PagePerkComponent,
    PerkComponent,
    StoreComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    routing
  ],
  providers: [
    PerksPredictionService,
    LcuConnectorService,
    StaticDataService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
