# Image Repository In a Split Service, Fully Containerized Model

This fully containerized solution utilizes three containers deployed under a single application with `docker-compose`. One container holds the `PostgreSQL` database while another holds a container which uses it's file system for image storage. The image storage container is packaged with a barebones front end for GUI interaction. The third container spins up to run tests on the endpoints at startup then terminates itself.

The solution currently implements two basic functions - storing an image with keywords/file name and retrieving a random image from the database based on supplied keywords.

## Running the Application

Running this application is very straightforward. 

Ensure that you have both `Docker` and `docker-compose` installed on your system. `Docker` install information can be found [here](https://docs.docker.com/engine/install/) and `docker-compose` install information can be found [here](https://docs.docker.com/compose/install/).

Pull this repo and navigate to it. Then run the following commands:

```shell
docker-compose build --no-cache
docker-compose up -d
```

After the containers spin up, you can check their status and ensure both containers are running with:

```shell
docker ps 
```

The application is set up to run on localhost and the barebones front end can be accessed via `0.0.0.0:8000`.

You can shut down the application at any time with:

```shell
docker-compose down
```

:warning: **Please ensure you have no local services overlapping with the services in the containers**: If you have a local instance of `uvicorn` or `PostgreSQL` running on default settings, you are best off stopping the services before running the `docker-compose` commands as the `docker-compose.yml` file port forwards default settings to your localhost for easy access and will overlap without changes. Example to shut down `PostgreSQL`:

```shell
sudo service postgresql stop
```

:warning: **The PostgreSQL container is set to persist**: The tests have a chance of failing if `docker-compose` is allowed to reuse old containers. You can remove all of your current docker containers (only do this if you don't have any containers on your machine you want to keep) with:

```shell
docker rm -vf $(docker ps -a -q)
```

## Testing the Application

During the `docker-compose` call that brings up the services, `docker-compose` will also spawn an `sut` service that will preform automated testing of the live endpoints. To see their status, you can check the docker container logs or run `docker-compose` without the `-d` option.

## Using the Application

The GUI it comes with (once you have navigated to it via the above section) is *incredibly* barebones, straightforward and simple. 

### To Upload an Image

Under the `Upload Image` heading, click `Choose File`.  Enter keywords seperated by spaces and press the `Submit` button directly below.  The next `html response` displays the `json` response returned by the server.

### Search for Images

Uder the `Search for Image Based on Attributes`, enter either a filename OR a string of keywords seperated by spaces.  Click the `Submit` button directly below the text boxes.  The server then displays the `file response` (in this case an image) to the `api` call.

## How it Works

### Storing an Image in the Repository

To store an image in this solution, a front end (in this case my barebones implementation) must provide an image file.  User can also (optionally) supply keywords which are attached to the image and can be used later for searching for and obtaining a random image from the repository. 

When the information is sent to the backend, it generateds a uuid for the image and grabs the file name as it was uploaded.  It then takes these two pieces of information and along with any optional tags, creates a entry in a seperate `PostgreSQL` service.  It also takes the image files, renames them to their uuid and stores them in a filesystem.  This model provides not only efficent searching and retrival of images, but prevents having to store images as information in a `PostgreSQL` type.

### Retriving an Image

Retriving an image requires the front end to send either a file name or a string of tags seperated by spaces.  If both are provided, the backend will default to providing an image based on the name.  Using the supplied information, it selects a randomized record from the database container.  The uuid in the retrived record points to a file name in the file system image storage and allows the return of the requested image.

## Moving Forward

:white_flag: Please note that this section purposefully omits front end improvements (although I'm sure I could find an engineer who, in exchange for a coffee/doughnut, would agree to argue it is sufficient as is).

If I took this project further, I would probably aim my focus at the following three areas.

### Security

There are some major security issues which should be addressed in taking this further, the most prevelant being the file server doesn't actually prevent you from uploading a cleverly named non-image file. The second most being it does not check the image itself for anything illegal or of poor taste, which is a catch 22 of the fun "get me a random image" nature of the implementation.

### User Authentication

Using OAuth 2.0 (or some other form of user authentication) would allow me to retrieve images based on users/groups and allow users/groups to block/restrict access to their images.  It could be useful in preventing unwanted images or implementing friend based random image retrieval.

### Inablity to Delete Images

Although the db administrator (or anyone who managed to obtain/guess the password) can delete images, users may want the ability to do so.  HOWEVER, I think baring VERY well implemented image filters (possibly to the point of fiction but thats another discussion) it might be fun to just have a database of pictures that people can add to and retrieve at random based on key words (I'm picturing the `gif` feature on `Slack`).
