import { inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

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
}
