interface Comments  {
    comment:string;
    blog:number;
}

interface Tags{
    tag:string;
}

export interface Blog{
    id:number;
    title:string;
    publication_date:Date;
    author:string;
    category:string;
    status:string;
    blog_content:string;
    tags:Tags[];
    comments:Comments[];
}

export interface ApiResponse {
    message: string;
    data: {
      count: number;
      data: Blog[];
    };
}
  