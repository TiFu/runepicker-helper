import { RouterModule, Route} from '@angular/router';
import { ModuleWithProviders } from '@angular/core';

import { RunePickerComponent } from './rune-picker/rune-picker.component';

export const routing: ModuleWithProviders = RouterModule.forRoot([
  { path:'', component: RunePickerComponent},
  { path: '**', redirectTo:''}
])
