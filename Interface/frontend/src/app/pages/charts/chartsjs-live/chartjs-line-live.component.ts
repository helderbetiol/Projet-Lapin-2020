import {Component, OnDestroy} from '@angular/core';
import {NbThemeService, NbColorHelper} from '@nebular/theme';
import {InfluxQueryService} from '../../../services/influx.service';

@Component({
  selector: 'ngx-chartjs-line-live',
  styleUrls: ['./chartjs-live.component.scss'],
  templateUrl: './chartjs-live.component.html',
})
export class ChartjsLineLiveComponent implements OnDestroy {
  data: any;
  colors: any;
  options: any;
  themeSubscription: any;
  selectedMeasure: any = 'adrenaline';
  selectedField: any = 'Tous';
  selectedGroup: any = 1;
  selectedLimit: any = '100';
  labelsFrom: any;
  labelsTo: any;
  dataPointsFCFrom: any;
  dataPointsFCTo: any;
  dataPointsFRFrom: any;
  dataPointsFRTo: any;
  dataPointsPAFrom: any;
  dataPointsPATo: any;
  timeLeft: number = 60;
  interval;
  startBtnStatus: any = 'primary';
  startBtnText: string = 'Démarrer';
  pauseBtnStatus: any = 'warning';
  pauseBtnText: string = 'Pause';
  paused: boolean = false;

  constructor(private theme: NbThemeService, private service: InfluxQueryService) {
    // this.updateData();

    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      this.colors = config.variables;
      const chartjs: any = config.variables.chartjs;

      this.options = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1,
        },
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
    clearInterval(this.interval);
    this.pauseBtnText = 'Continuer';
    this.pauseBtnStatus = 'primary';
    this.paused = true;
    this.selectedField = newValue;
  }

  changeGroup(newValue): void {
    this.selectedGroup = newValue;
  }

  changeLimit(newValue): void {
    this.selectedLimit = newValue;
  }

  applySelection() {
    if (this.startBtnStatus === 'primary') {
      this.startBtnStatus = 'danger';
      this.startBtnText = 'Redémarrer';
    } else {
      clearInterval(this.interval);
    }
    this.updateData();
    this.paused = false;
    this.pauseBtnText = 'Pause';
    this.pauseBtnStatus = 'warning';
  }

  updateData() {
    this.service.getData(this.selectedMeasure, this.selectedGroup, 'PressionArterielle', this.selectedLimit)
      .subscribe((data) => {
        let labels = [];
        let dataPoints = [];
        // @ts-ignore
        data.forEach((point) => {
          labels.push(point['time'].substring(14, 23));
          dataPoints.push(point['PressionArterielle']);
        });
        this.labelsFrom = labels.reverse();
        this.dataPointsPAFrom = dataPoints.reverse();
        this.labelsTo = [this.labelsFrom.pop()];
        this.dataPointsPATo = [this.dataPointsPAFrom.pop()];

        this.service.getData(this.selectedMeasure, this.selectedGroup, 'FrequenceCardiaque', this.selectedLimit)
          .subscribe((data) => {
            labels = [];
            dataPoints = [];
            // @ts-ignore
            data.forEach((point) => {
              dataPoints.push(point['FrequenceCardiaque']);
            });
            this.dataPointsFCFrom = dataPoints.reverse();
            this.dataPointsFCTo = [this.dataPointsFCFrom.pop()];

            this.service.getData(this.selectedMeasure, this.selectedGroup, 'FrequenceRespiratoire', this.selectedLimit)
              .subscribe((data) => {
                labels = [];
                dataPoints = [];
                // @ts-ignore
                data.forEach((point) => {
                  dataPoints.push(point['FrequenceRespiratoire']);
                });
                this.dataPointsFRFrom = dataPoints.reverse();
                this.dataPointsFRTo = [this.dataPointsFRFrom.pop()];

                this.updateChartData();
                this.startTimer();
              });
          });
      });
  }

  startTimer() {
    this.interval = setInterval(() => {
      if (this.timeLeft > 0) {
        this.timeLeft--;
        this.labelsTo.push(this.labelsFrom.pop());
        this.dataPointsFCTo.push(this.dataPointsFCFrom.pop());
        this.dataPointsFRTo.push(this.dataPointsFRFrom.pop());
        this.dataPointsPATo.push(this.dataPointsPAFrom.pop());
        this.updateChartData();
      } else {
        this.timeLeft = 60;
      }
    }, 1500);
  }

  pauseTimer() {
    if (!this.paused) {
      clearInterval(this.interval);
      this.pauseBtnText = 'Continuer';
      this.pauseBtnStatus = 'primary';
      this.paused = true;
    } else {
      this.startTimer();
      this.pauseBtnText = 'Pause';
      this.pauseBtnStatus = 'warning';
      this.paused = false;
    }
  }

  updateChartData() {
    if (this.selectedField === 'PressionArterielle') {
      this.updateChartDataField('PressionArterielle', this.dataPointsFRTo);
    } else if (this.selectedField === 'FrequenceCardiaque') {
      this.updateChartDataField('FrequenceCardiaque', this.dataPointsFRTo);
    } else if (this.selectedField === 'FrequenceRespiratoire') {
      this.updateChartDataField('FrequenceRespiratoire', this.dataPointsFRTo);
    } else {
      this.updateChartDataAll();
    }
  }

  updateChartDataAll() {
    this.data = {
      labels: this.labelsTo,
      datasets: [{
        data: this.dataPointsFCTo,
        label: 'FrequenceCardiaque',
        backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
        borderColor: this.colors.primary,
      },
        {
          data: this.dataPointsPATo,
          label: 'PressionArterielle',
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.danger, 0.3),
          borderColor: this.colors.danger,
        }, {
          data: this.dataPointsFRTo,
          label: 'FrequenceRespiratoire',
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.info, 0.3),
          borderColor: this.colors.info,
        },
      ],
    };
  }

  updateChartDataField(field, data) {
    this.data = {
      labels: this.labelsTo,
      datasets: [{
        data: data,
        label: field,
        backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
        borderColor: this.colors.primary,
      }],
    };
  }
}
