#RUN

docker run -p 5000:5000 --name insta -v `pwd`/zip:/code/results instagram-fetcher
