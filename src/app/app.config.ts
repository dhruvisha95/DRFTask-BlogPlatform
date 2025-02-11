import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { AuthInterceptor } from './auth/auth.interceptor';
import { HTTP_INTERCEPTORS, withInterceptors, withInterceptorsFromDi } from '@angular/common/http';
import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient(
    withInterceptorsFromDi(),
  ),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
   ]
};
