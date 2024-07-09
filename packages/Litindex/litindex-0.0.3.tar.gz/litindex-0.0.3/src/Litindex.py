from selectolax.lexbor import LexborHTMLParser
from urllib.parse import  quote
from pydantic import BaseModel
from src.exception import NotFoundError
import aiohttp
import asyncio
 
class Litindex:
    def __init__(self,*,search:str) -> None:
        '''
        Args:
            search (str): _description_
        Returns:
            None
        '''
        self.res_url = "https://openlibrary.org/search?q={}&mode=everything".format(quote(search))
        asyncio.run(self._get(self.res_url))
        
    async def _get(self,url) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response: 
                self.html = await response.text()
                self.parser = LexborHTMLParser(self.html)
                self.status = response.status

    def books(self,*,page:int=1) -> list:
        """
        Args:
            page (int, optional): _description_. Defaults to 1.

        Returns:
            list: _description_
        """
        if page == 1:
            self._books=[
                {
                    book.css_first("div.resultTitle a").text(strip=True):
                    "https://openlibrary.org{}".format(
                            book.css_first("div.details a").attrs["href"]
                        )
                    } for book in self.parser.css("ul.list-books li")
            ]
            

        elif page>1:
            self._books=[]
            for p in range(1,page+1):
                asyncio.run(self._get(self.res_url+"&page={}".format(p)))
                for book in self.parser.css("ul.list-books li"):
                    self._books.append(
                        {
                        book.css_first("div.resultTitle a").text(strip=True):
                        "https://openlibrary.org{}".format(
                                book.css_first("div.details a").attrs["href"]
                                )
                            }   
                    )
        
            else:
                raise NotFoundError("the title is not found")
        
        return self._books
    
    def _bookinfo(self,title) -> LexborHTMLParser:
        """
        Args:
            title (str): _description_

        Raises:
            NotFoundError: _description_

        Returns:
            LexborHTMLParser: _description_
        """
        if self._books:
            self._title=title
            self._url=''.join(list(t.values())[0] for t in self._books if self._title==list(t.keys())[0]) 
            if self._url:
                asyncio.run(self._get(self._url))
                return self.parser
            else:
                raise NotFoundError("the title is not found")
    @property
    def hit(self) -> str:
        '''hits of the book'''
        hits = self.parser.css_first("div.search-results-stats").text(strip=True,deep=False)
        return ''.join(hits)  
            
    
    def title(self,*,_title:str) -> str:
        ''' title of the book '''
        title={}

        title.update(
            title=_title
        )

        return title
    
    def rate(self,*,_title:str) -> dict:
        ''' rate of the book '''
        rate_={}
        perser=self._bookinfo(_title)
        ratingvalues=perser.css_first('li.avg-ratings span[itemprop="ratingValue"]')
        ratings_avgs=perser.css_first('li.readers-stats__review-count')

        if ratingvalues and ratings_avgs:

            rate_.update(
                    rating=ratings_avgs.text(strip=True)+'/5.0',
                    rate=ratingvalues.text(strip=True),
                )
        
        else:
            rate_.update(
                rating='NoInformation',
                rate='NoInformation',
            )
        
        return rate_
    def author(self,*,_title:str) -> dict:
        ''' author of the book '''
        author_={}
        perser=self._bookinfo(_title)
        author_name=perser.css_first('h2.edition-byline a[itemprop="author"]')

        if author_name:
            author_.update(
                author=author_name.text(strip=True)
            )

        else:
            author_.update(
                author='NoInformation'
            )

        return author_
    
    def description(self,*,_title:str) -> str:
        ''' description of the book '''
        description_={}
        perser=self._bookinfo(_title)
        description_name=perser.css_first('div.book-description p')

        if description_name:
            description_text=description_name.text(strip=True)
            description_.update(
                description=description_text
            )
            
        else:
            description_.update(
                description='NoInformation'
            )

        return description_
    
    def publisher(self,*,_title:str) -> dict:
        ''' publisher of the book '''
        publisher={}
        perser=self._bookinfo(_title)
        publisher_name=perser.css_first('a[itemprop="publisher"]')
        publisher_url=perser.css_first('a[itemprop="publisher"]')

        if publisher_name and publisher_url:

            publisher.update(
                publisher=publisher_name.text(strip=True),
                url="https://openlibrary.org"+publisher_url.attrs['href']
            )
        else:
            publisher.update(
                publisher='NoInformation',
                url='NoInformation'
            )

        return publisher
    
    def language(self,*,_title:str) -> dict:
        ''' language of the book '''
        language={}
        perser=self._bookinfo(_title)
        language_name=perser.css_first('span[itemprop="inLanguage"] a')

        if language_name:
            language_text=language_name.text(strip=True)
            language.update(
                language=language_text
            )
        else:
            language.update(
                language='NoInformation'
            )

        return language
    
    def pages(self,*,_title:str) -> dict:
        ''' pages of the book '''
        pages={}
        perser=self._bookinfo(_title)
        pages_=perser.css_first('div.edition-omniline-item span[itemprop="numberOfPages"]')

        if pages_:
            pages_text=pages_.text(strip=True)
            pages.update(
                pages=pages_text
            )
        else:
            pages.update(
                pages='NoInformation'
            )

        return pages
    
    def publish_date(self,*,_title:str) -> dict:
        ''' publish_date of the book '''
        publish_date={}
        perser=self._bookinfo(_title)
        publish_date_=perser.css_first('span[itemprop="datePublished"]')

        if publish_date_:
            publish_date_text=publish_date_.text(strip=True)
            publish_date.update(
                PublishDate=publish_date_text
            )
        else:
            publish_date.update(
                PublishDate='NoInformation'
            )

        return publish_date
    
    def series(self,*,_title:str) -> dict:
        ''' series of the book '''
        series={}
        perser=self._bookinfo(_title)
        series_=perser.css_first('dl.meta dd.object')

        if series_:
            if series_.text(strip=True)=='Series':
                series.update(
                    series=series_
                )

        else:
            series.update(
                series='NoInformation'
            )

        return series