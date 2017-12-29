import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PerksPickerComponent } from './perks-picker.component';

describe('PerksPickerComponent', () => {
  let component: PerksPickerComponent;
  let fixture: ComponentFixture<PerksPickerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PerksPickerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PerksPickerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
