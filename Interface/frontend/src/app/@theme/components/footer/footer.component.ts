import { Component } from '@angular/core';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span class="created-by">
      Created with ♥ by Group Projet Lapin 2020-2021 based on templates by <b><a href="https://akveo.page.link/8V2f" target="_blank">Akveo</a></b>
    </span>
  `,
})
export class FooterComponent {
}
