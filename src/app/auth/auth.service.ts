import { inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({
    providedIn:'root'
})


export class AuthService{

    http = inject(HttpClient)

    login(email:string, password:string){
        this.http.post('http://127.0.0.1:8000/api/login/',{email,password}).subscribe(config => {
            console.log('Updated config:', config);
          });
    }
}
