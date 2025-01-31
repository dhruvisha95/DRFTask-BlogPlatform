import { Routes } from '@angular/router';
import { RegisterComponent } from './auth/register/register.component';
import { BlogsComponent } from './blogs/blogs.component';
import { BlogComponent } from './blogs/blog/blog.component';

export const routes: Routes = [
        {path:'auth' , loadChildren: () => import('./auth/auth-routing.module').then((m)=>m.AuthRoutingModule)},
        {path:'register', component:RegisterComponent},
        {path:'blogs' , component:BlogsComponent},
        {path:'blog/:id', component:BlogComponent}
];
