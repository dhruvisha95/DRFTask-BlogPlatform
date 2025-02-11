import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import {FormGroup, FormControl} from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {

  httpClient = inject(HttpClient)

  constructor(private authService:AuthService){}

  loginForm = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''),
  });


  onSubmit(){
    console.warn(this.loginForm.value);
    const { email, password } = this.loginForm.value;

    this.authService.login(email!,password!);
  }
}
