interface Comments  {
    comment:string;
    blog:number;
}

export interface Tags{
    tag:string;
}

export interface Blog{
    id?:number;
    title?:string;
    publication_date?:Date;
    author?:number;
    category?:number;
    status?:string;
    blog_content?:string;
    tags?:Tags[];
    comments?:Comments[]|null;
}

  