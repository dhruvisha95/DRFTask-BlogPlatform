import { inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Blog } from "./blog.model";
import { Title } from "@angular/platform-browser";

@Injectable({
    providedIn:'root'
})

export class BlogService{

    http = inject(HttpClient)

    getBlogs():Observable<any>{
        return this.http.get('http://127.0.0.1:8000/api/blogs/')
    }

    getBlogsWithId(id:number):Observable<any>{
        return this.http.get('http://127.0.0.1:8000/api/blogs/'+id)
    }

    postBlog(blog:Blog|null):Observable<any>{
        let bloga = {
            author:1,
            title:"ii",
            publication_date: new Date(),
            category:2,
            tags:[{'tag':'java'}],
            blog_content:"this.blogForm.value.blog_content",
            status: "draft",
        }
        return this.http.post('http://127.0.0.1:8000/api/blogs/',blog)
    }
}
