import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse, HttpHeaders, HttpParams} from '@angular/common/http';
import { environment } from '../../environments/environment';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';


// /** InfluxDB v2 URL */
// const url = process.env['INFLUX_URL'] || 'http://localhost:8086';
// /** InfluxDB authorization token */
// const token = process.env['INFLUX_TOKEN'] || 'my-token';
// /** Organization within InfluxDB  */
// const org = process.env['INFLUX_ORG'] || 'my-org';
// /**InfluxDB bucket used in examples  */
// const bucket = 'my-bucket';
// // ONLY onboarding example
// /**InfluxDB user  */
// const username = 'root';
// /**InfluxDB password  */
// const password = 'root';
const headers = new HttpHeaders().set('Content-Type', 'application/vnd.flux').set('Accept', 'application/csv').set('Access-Control-Allow-Origin', '*');
@Injectable({
  providedIn: 'root',
})
export class ServerService {
  private baseUrl =  'https://lapin-influx.osc-fr1.scalingo.io/';

  constructor(private http: HttpClient) { }

  get = <T>(extension, params = null) => {
    return this.http.get<T>(this.baseUrl + extension, this.getParams(params)).pipe(catchError(this.handleError));
  }

  post = <T>(extension, data = {}) => {
    const options = { headers: headers };
    return this.http.post<T>(this.baseUrl + extension, data, options).pipe(catchError(this.handleError));
  }

  delete = (extension) => {
    return this.http.delete(this.baseUrl + extension, this.getParams()).pipe(catchError(this.handleError));
  }

  put = <T>(extension, data, params = null) => {
    return this.http.put<T>(this.baseUrl + extension, data, this.getParams(params)).pipe(catchError(this.handleError));
  }

  handleError = (error: HttpErrorResponse) => {
    return throwError(error.message || 'Error');
  }

  private getParams = (params = null) => {
    if (!params) {
      params = new HttpParams();
    }
    return { params };
  }
}
