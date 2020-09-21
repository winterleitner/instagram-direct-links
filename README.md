#Instagram Fetcher

Python (Flask) web app that takes a list of instagram post urls from a csv file and returns a zip archive of a csv with all direct image links and the images themselves.


#Usage
```curl
curl --location --request POST 'localhost:5000' --form 'file=@PATH_TO_CSV'
```

# Download

Get a pre-built docker image from:

https://hub.docker.com/r/winterleitner/instagram-fetcher

#RUN
docker run -p 5000:5000 --name seltat/instagram_fetcher -v `pwd`/zip:/code/results instagram-fetcher
