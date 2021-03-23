# Lapin Dashboard

Lapin Dashboard is the frontend of the Lapin Project 2020-2021 at IMT Atlantique. The purpose of this interface is to display the measurements obtained in previous TPs (Pratical Work) with live rabbits in the school of veterinary and display newly generated measurements by LoudML to simulate a new TP without the use of a rabbit.

## Getting started with the code
To begin, go straight to src/app/pages, there you will find:
- pages-routing.module.ts: redirects empty path (home) to charts/chartjs.
- pages-menu.ts: where each option of the left menu will redirect you too.
- charts/chartjs
  - charts.component.html + charts.component.scss + charts-line.component.html: component for "Graphiques" to show statically the measures get from the backend as a line graph.
  - chartsjs-live:  component for "LIVE" to show dynamically the measures get from the backend as a live line graph, a new point added each X seconds (configurable).

And how do we get the data from the backend?
- src/app/services contains a server service to send and receive HTTP requests and an influx service to create the requests.

## Angular

This project was built in Angular, learn the basics:

### Prerequisites

- Node.js: Angular requires a [current, active LTS, or maintenance LTS](https://nodejs.org/about/releases) version of Node.js.
- npm package manager: Angular, the Angular CLI, and Angular applications depend on npm packages for many features and functions. To check that you have the npm client installed, run npm -v in a terminal window. To install it, go [here](https://docs.npmjs.com/cli/install).
- [Angular CLI](https://github.com/angular/angular-cli): necessary for development. It can be installed with the command `npm install -g @angular/cli`.

Source and more info: [Angular Setup Guide](https://angular.io/guide/setup-local)
### Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

### Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

### Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

### Further help with Angular

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.

## ngx-admin [<img src="https://i.imgur.com/oMcxwZ0.png" alt="Eva Design System" height="20px" />](https://eva.design?utm_campaign=eva_design%20-%20home%20-%20ngx_admin%20github%20readme&utm_source=ngx_admin&utm_medium=referral&utm_content=top_status_tile)

This dashboard was created using ngx-admin by [Akveo team](https://www.akveo.com?utm_campaign=services%20-%20akveo%20website%20-%20ngx_admin%20github%20readme&utm_source=ngx_admin&utm_medium=referral&utm_content=from_developers_made_by) as a template. 

[Documentation](https://akveo.github.io/ngx-admin?utm_campaign=ngx_admin%20-%20home%20-%20ngx_admin%20github%20readme&utm_source=ngx_admin&utm_medium=referral&utm_content=github_readme_documentation_link) | [Installation Guidelines](https://akveo.github.io/ngx-admin/docs/getting-started/what-is-ngxadmin?utm_campaign=ngx_admin%20-%20home%20-%20ngx_admin%20github%20readme&utm_source=ngx_admin&utm_medium=referral&utm_content=github_readme_installation_guidelines) | [Angular templates](https://www.akveo.com/templates?utm_campaign=services%20-%20github%20-%20templates&utm_source=ngx_admin&utm_medium=referral&utm_content=github%20readme%20top%20angular%20templates%20link)

### Key features

- The most popular and trusted Angular open source dashboard template is out there. Used by hundreds of thousands developers worldwide and Fortune 500 companies*.
- Over 40+ Angular Components and 60+ Usage Examples. Kick off your project and save money by using ngx-admin.
- ngx-admin material works perfectly with Angular Material and Nebular. Take the best from both!

### What's included:

- Angular 10+ & Typescript
- Bootstrap 4+ & SCSS
- Responsive layout
- RTL support
- High resolution
- Flexibly configurable themes with **hot-reload** (3 themes included)
- Authentication module with multiple providers
- 40+ Angular Components
- 60+ Usage Examples

### Complete demo of the template

<a target="_blank" href="http://www.akveo.com/ngx-admin/?utm_campaign=ngx_admin%20-%20demo%20-%20ngx_admin%20github%20readme&utm_source=ngx_admin&utm_medium=referral&utm_content=live_demo_link">Live Demo</a>

### More documentation
This template is using [Nebular](https://github.com/akveo/nebular) modules set, [here you can find documentation and other useful articles](https://akveo.github.io/nebular/docs/guides/install-based-on-starter-kit?utm_campaign=nebular%20-%20docs%20-%20ngx_admin%20github%20readme&utm_source=ngx_admin&utm_medium=referral&utm_content=documentation_useful_articles).
