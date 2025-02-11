import { Component, signal } from '@angular/core';
import { Blog, Tags } from '../blog.model';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { BlogService } from '../blog.service';

@Component({
  selector: 'app-blog-post',
  imports: [ReactiveFormsModule],
  standalone:true,
  templateUrl: './blog-post.component.html',
  styleUrl: './blog-post.component.css'
})

export class BlogPostComponent {

  constructor(private blogService:BlogService){}
  blog = signal<Blog|null>(null);

  blogForm = new FormGroup({
    id: new FormControl<number|undefined>(undefined),
    title: new FormControl('', { nonNullable: true }),
    publication_date: new FormControl<Date>(new Date(),{ nonNullable: true }),
    author: new FormControl<string>('', { nonNullable: true }),
    category: new FormControl<string>('', { nonNullable: true }),
    status: new FormControl('', { nonNullable: true }),
    blog_content: new FormControl('', { nonNullable: true }),
    tags:new FormControl<Tags[]>([], { nonNullable: true }),
  })

  submitBlog(){

    this.blog.set({
      author:1,
      title:this.blogForm.value.title,
      publication_date:this.blogForm.value.publication_date,
      category:2,
      tags:[{'tag':'java'}],
      blog_content:this.blogForm.value.blog_content,
      status:this.blogForm.value.status,
    })

    this.blogService.postBlog(this.blog()).subscribe((res)=>{console.log(res)})
    console.log(this.blogForm.value)
  }
}
