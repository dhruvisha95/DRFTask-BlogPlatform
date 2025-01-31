import { Component, computed, inject, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavComponent } from './nav/nav.component';
import { Router } from '@angular/router';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,NavComponent,NgIf],
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {
  title = 'project-blogapp';

  private router = inject(Router)
  route = signal(this.router.url);
  check = computed(()=>this.route()==='/')

  constructor(){
    this.router.events.subscribe(()=>{
      this.route.set(this.router.url)
    })
  }
}
