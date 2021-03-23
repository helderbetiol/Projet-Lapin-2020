import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ChartsComponent } from './charts.component';
import { EchartsComponent } from './echarts/echarts.component';
import { D3Component } from './d3/d3.component';
import {ChartjsLineComponent} from './chartjs/chartjs-line.component';
import {ChartjsLineLiveComponent} from './chartsjs-live/chartjs-line-live.component';

const routes: Routes = [{
  path: '',
  component: ChartsComponent,
  children: [{
    path: 'echarts',
    component: EchartsComponent,
  }, {
    path: 'd3',
    component: D3Component,
  }, {
    path: 'chartjs',
    component: ChartjsLineComponent,
  }, {
    path: 'chartjs-live',
    component: ChartjsLineLiveComponent,
  }
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ChartsRoutingModule { }

export const routedComponents = [
  ChartsComponent,
  EchartsComponent,
  D3Component,
  ChartjsLineComponent,
  ChartjsLineLiveComponent,
];
