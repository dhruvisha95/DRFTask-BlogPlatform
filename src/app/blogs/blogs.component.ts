import { Component, inject, OnInit, signal } from '@angular/core';
import { Blog } from './blog.model';
import { BlogService } from './blog.service';
import { NgFor } from '@angular/common';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-blogs',
  imports: [NgFor, DatePipe],
  templateUrl: './blogs.component.html',
  styleUrl: './blogs.component.css',
  standalone: true
})

export class BlogsComponent implements OnInit{
  blogs = signal<Blog[] | undefined>(undefined);
  private router = inject(Router)

  constructor(private blogService:BlogService){}

  ngOnInit(): void {
      this.blogService.getBlogs().subscribe((res)=>{
        this.blogs.set(res.data.data)
      })
  }

  handleClick(blog:Blog){
      this.router.navigate(['blog/',blog.id])
  }
}
