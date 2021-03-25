import { Component, Input } from '@angular/core';
import { NbSortDirection, NbSortRequest, NbTreeGridDataSource, NbTreeGridDataSourceBuilder } from '@nebular/theme';
import {InfluxQueryService} from '../../../services/influx.service';

interface TreeNode<T> {
  data: T;
  children?: TreeNode<T>[];
  expanded?: boolean;
}

interface FSEntry {
  name: string;
  size: string;
  kind: string;
  items?: number;
}

@Component({
  selector: 'ngx-tree-grid',
  templateUrl: './tree-grid.component.html',
  styleUrls: ['./tree-grid.component.scss'],
})
export class TreeGridComponent {
  customColumn = 'name';
  defaultColumns = [ 'size', 'kind', 'items' ];
  allColumns = [ this.customColumn, ...this.defaultColumns ];

  dataSource: NbTreeGridDataSource<FSEntry>;

  sortColumn: string;
  sortDirection: NbSortDirection = NbSortDirection.NONE;

  constructor(private dataSourceBuilder: NbTreeGridDataSourceBuilder<FSEntry>,
              private service: InfluxQueryService) {
    this.dataSource = this.dataSourceBuilder.create(this.data);
  }

  updateSort(sortRequest: NbSortRequest): void {
    this.sortColumn = sortRequest.column;
    this.sortDirection = sortRequest.direction;
  }

  getSortDirection(column: string): NbSortDirection {
    if (this.sortColumn === column) {
      return this.sortDirection;
    }
    return NbSortDirection.NONE;
  }

  private data: TreeNode<FSEntry>[] = [
    {
      data: { name: 'Adrenaline', size: '1.8 MB', items: 5, kind: 'dir' },
      children: [
        { data: { name: 'Adrenaline-group1-22-03-2016', kind: 'csv', size: '240 KB' } },
        { data: { name: 'Adrenaline-group2-22-03-2016', kind: 'csv', size: '290 KB' } },
        { data: { name: 'Adrenaline-group3-22-03-2016', kind: 'csv', size: '466 KB' } },
        { data: { name: 'Adrenaline-group4-22-03-2016', kind: 'csv', size: '900 KB' } },
      ],
    },
    {
      data: { name: 'Fréquence Cardiaque', kind: 'dir', size: '400 KB', items: 2 },
      children: [
        { data: { name: 'Fréquence Cardiaque-group1-22-03-2016', kind: 'csv', size: '100 KB' } },
        { data: { name: 'Fréquence Cardiaque-group2-22-03-2016', kind: 'csv', size: '300 KB' } },
      ],
    },
    {
      data: { name: 'Fréquence Respiratoire', kind: 'dir', size: '109 MB', items: 2 },
      children: [
        { data: { name: 'Fréquence Respiratoire-group1-22-03-2016', kind: 'csv', size: '107 MB' } },
        { data: { name: 'Fréquence Respiratoire-group2-22-03-2016', kind: 'csv', size: '2 MB' } },
      ],
    },
  ];

  getShowOn(index: number) {
    const minWithForMultipleColumns = 400;
    const nextColumnStep = 100;
    return minWithForMultipleColumns + (nextColumnStep * index);
  }

  downloadCSV(fileName: any) {
    var temp = fileName.split("-");
    var selectedMeasure = temp[0];
    var selectedGroup = '';
    for (let i=5; i < temp[1].length; i++)
    {
      selectedGroup += temp[1].charAt(i);
    }
    console.log('downloadCSV');
    return this.service.getCSV(selectedMeasure, selectedGroup);
  }

  /* downloadCSV(fileName: any, selectedMeasure: any, selectedGroup: any) {
    console.log('downloadCSV');
    this.service.getCSV(selectedMeasure, selectedGroup)
      .subscribe((file) => {
        console.log("got file");
        console.log(file);
      const binaryFile = [];
      binaryFile.push(file);
      //const filePath = URL.createObjectURL(file);
      const filePath = URL.createObjectURL(new Blob(binaryFile, {type: 'aplication/csv'}));
      const hrefLink = document.createElement('a');
      hrefLink.href = filePath;
      hrefLink.setAttribute('download', fileName);
      document.body.appendChild(hrefLink);
      hrefLink.click();
    });
  }*/

}

@Component({
  selector: 'ngx-fs-icon',
  template: `
    <nb-tree-grid-row-toggle [expanded]="expanded" *ngIf="isDir(); else fileIcon">
    </nb-tree-grid-row-toggle>
    <ng-template #fileIcon>
      <nb-icon icon="file-text-outline"></nb-icon>
    </ng-template>
  `,
})
export class FsIconComponent {
  @Input() kind: string;
  @Input() expanded: boolean;

  isDir(): boolean {
    return this.kind === 'dir';
  }
}
