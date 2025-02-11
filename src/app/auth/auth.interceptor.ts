import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    console.log("hello")
    const authToken = localStorage.getItem('authToken');

    // if (authToken) {
      req = req.clone({
        setHeaders: {
          Authorization: 'Token 1b013993cc2cdc610d66ff02a4b139274361fcc8'
        }
      });
    // }

    return next.handle(req);
  }
}
