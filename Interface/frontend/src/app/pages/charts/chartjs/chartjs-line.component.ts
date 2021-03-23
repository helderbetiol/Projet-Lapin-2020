import { Component, OnDestroy } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import {InfluxQueryService} from '../../../services/influx.service';

@Component({
  selector: 'ngx-chartjs-line',
  styleUrls: ['./chartjs.component.scss'],
  templateUrl: './chartjs.component.html',
  // selector: 'ngx-chartjs-line',
  // template: `
  //   <chart type="line" [data]="data" [options]="options"></chart>
  // `,
})
export class ChartjsLineComponent implements OnDestroy {
  data: any;
  colors: any;
  options: any;
  themeSubscription: any;
  selectedMeasure: any = 'adrenaline';
  selectedField: any = 'FrequenceCardiaque';
  selectedGroup: any = 1;
  selectedLimit: any = '10';

  constructor(private theme: NbThemeService, private service: InfluxQueryService) {
    this.updateData();
    // this.service.getData().subscribe((data) => {
    //   console.log(data);
    //
    //   const labels = [];
    //   const dataPoints = [];
    //   // @ts-ignore
    //   data.forEach((point) => {
    //     labels.push(point['time']);
    //     dataPoints.push(point['FrequenceCardiaque']);
    //   });
    //
    //   console.log(labels);
    //   console.log(dataPoints);
    //
    //   this.data = {
    //     labels: labels,
    //     datasets: [{
    //       data: dataPoints,
    //       label: 'Lapin 1',
    //       backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
    //       borderColor: this.colors.primary,
    //     },
    //     ],
    //   };
    // });

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      this.colors = config.variables;
      const chartjs: any = config.variables.chartjs;

      this.options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              gridLines: {
                display: true,
                color: chartjs.axisLineColor,
              },
              ticks: {
                fontColor: chartjs.textColor,
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: chartjs.axisLineColor,
              },
              ticks: {
                fontColor: chartjs.textColor,
              },
            },
          ],
        },
        legend: {
          labels: {
            fontColor: chartjs.textColor,
          },
        },
      };
    });
  }

  ngOnDestroy(): void {
    this.themeSubscription.unsubscribe();
  }

  changeMeasure(newValue): void {
    this.selectedMeasure = newValue;
  }
  changeField(newValue): void {
    this.selectedField = newValue;
  }
  changeGroup(newValue): void {
    this.selectedGroup = newValue;
  }
  changeLimit(newValue): void {
    this.selectedLimit = newValue;
  }

  applySelection() {
    this.updateData();
  }

  updateData() {
    this.service.getData(this.selectedMeasure, this.selectedGroup, this.selectedField, this.selectedLimit)
      .subscribe((data) => {
      console.log(data);

      const labels = [];
      const dataPoints = [];
      // @ts-ignore
      data.forEach((point) => {
        labels.push(point['time'].substring(14, 23));
        dataPoints.push(point[this.selectedField]);
      });

      console.log(labels);
      console.log(dataPoints);

      this.data = {
        labels: labels,
        datasets: [{
          data: dataPoints,
          label: 'Lapin '+this.selectedGroup+' '+this.selectedMeasure+' '+this.selectedField ,
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
          borderColor: this.colors.primary,
        },
        ],
      };
    });
  }

}
