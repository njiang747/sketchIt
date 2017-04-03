# sketchIt

## Inspiration
Today the web is filled with millions of images. The way we use the internet has changed dramatically over the last couple years, yet the way we search for images has not. Have you ever had a specific image in mind-- it's right there in front of you, but you just can't seem to describe it in a way that Google Images understands? With SketchIt, those days are no more.

## What it does
SketchIt allows you to draw an image and will return to you pictures that match your query. Looking for a picture of a pencil facing diagonally downwards? Easy. How about four fish stacked on top of each other? No problem. If you can imagine it, SketchIt will find it.

## How we built it
We built the entire application almost from scratch. The main logic is written in Python and the only external library we use is OpenCV to generate the Canny Edge representation of images. The basic logic is as follows:

Given an input sketch S, we want to match it to one of the images stored in our database, D.
We pre-process "hit maps" of each image based on their Canny Edge representation. The map essentially allows users a margin of error so that as long as their sketch falls within the map, it is still considered a match.
We then look at our database of images and return the images with the most matches
In order to further strengthen the matching we then do a reverse comparison from D -> S, in which we generate a hitmap based off the input sketch S and try to map the images from the previous step to S's hit map.
Users can supply an optional "tag" query to aid their sketch. For instance, if the user drew a chicken, they can also supply the tag "bird" to narrow down the searching space
Our database was built by scraping images from Bing using the Bing image search API. These images were then classified with tags using Microsoft Cognative Services' Vision API.

## Challenges we ran into
Since we implemented our algorithm basically from scratch, we ran into many many issues. One memorable problem we dubbed "Night Sky". Our algorithm was too sensitive to noise and as a result many images of the night sky would match everything because their hitmaps would cover the entire window.

Another hurdle we overcame was we were originally using sobel gradients to calculate the direction of each edge. This resulted in not so accurate directions. We then switched to convolution, which uses gradients of gaussians and drastically improved our results.

Lastly, scalibility was a large problem that we still have not completely overcome. Our database of images currently contains 8000 images. We would ideally have upwards of 2,000,000 images. Storing all those images and efficiently searching through them for each query in a reasonable amount of time was no easy task. In the end we used a reverse indexing in which we mapped every possible edge to a list of images that contained that edge. This provides efficient lookup times that were reasonable, but of course could always be improved.

## Accomplishments that we're proud of
SketchIt is still in its infancy, but it is able to reliably match a number of images. In the very beginning, we were trying to match hearts and we literally had to trace over an image and even then we'd be lucky if the algorithm would images with hearts. Now, even Jon, our team's worst artist is able to freehand hearts and have SketchIt return the right images.

We are also very proud of the speed of our application. It may not seem like much, but you have to remember that with every sketch query, the application has to compare pixel by pixel each edge of the query sketch with every other pixel in each of the 8,000 images in our database. The current implementation runs in under 5 seconds on our laptops, which is a huge improvement over the 16 minutes it originally took to run one query.

## What we learned
Efficiency is so important. When dealing with a large amount of data, the smallest changes can result in huge increases or decreases in runtime. Scalibility was definitely our biggest roadblock and once we realized this we were able to change the way we approached the problem.

## What's next for SketchIt
Improvements to the algorithm will allow us to improve our accuracy even more. The biggest issue we have right now is that we simply do not have enough images to search through. A larger database of images will also improve results drastically.

