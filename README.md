#Instagram Fetcher

Python (Flask) web app that takes a list of instagram post urls from a csv file and returns a zip archive of a csv with all direct image links and the images themselves.

###Disclaimer!
Using this software may violate Instagram's terms of service. This is only meant as a proof of concept.

#Usage
```curl
curl --location --request POST 'localhost:5000' --form 'file=@PATH_TO_CSV'
```

# Build
```console
docker build . -t instagram-fetcher
```

#Run
docker run -p 5000:5000 --name instagram_fetcher -v `pwd`/zip:/code/results instagram-fetcher


#License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.