import { Component, inject, OnInit, signal } from '@angular/core';
import { BlogService } from '../blog.service';
import { ActivatedRoute } from '@angular/router';
import { Blog } from '../blog.model';
import { NgFor } from '@angular/common';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-blog',
  imports: [NgFor,DatePipe],
  templateUrl: './blog.component.html',
  styleUrl: './blog.component.css'
})


export class BlogComponent implements OnInit{

  constructor(private blogService:BlogService){}
  private route = inject(ActivatedRoute)

  blog = signal<Blog|undefined>(undefined);

  ngOnInit(): void {
    
    const id = Number(this.route.snapshot.paramMap.get('id'))
    this.blogService.getBlogsWithId(id).subscribe((res)=>{
      this.blog.set(res.data)

    })

  }

}
