# Image library

**"Image library"** is an application that allows users to manage their images. The application provides users, depending on their account configuration, such feature as:

- Uploading images in .png and .jpg formats.
- Access to thumbnails in predefined sizes and the original image.
- Fetching expiring links for image downloads.

There are three built-in tiers:

- **"Basic"** access:
  - a link to a thumbnail that's 200px in height
- **"Premium"** access:
  - a link to a thumbnail that's 200px in height
  - a link to a thumbnail that's 400px in height
  - a link to the originally uploaded image
- **"Enterprise"** access: - a link to a thumbnail that's 200px in height - a link to a thumbnail that's 400px in height - a link to the originally uploaded image - ability to fetch an expiring link to the image (the link expires after a given number of seconds (the user can specify any number between 300 and 30000))
  Furthermore, admins have the flexibility to customize user accounts to their preferences.

The user interface is built using the browsable API of Django Rest Framework, while the admin UI is developed within django-admin.

## How to run this project?

### Development

Uses the default Django develompment server.

1. Rename .env.dev.sample to .env
2. Update enviroment variable to fit your needs.
3. Build the images and run containers:
   ```
   $ docker-compose up -d --build
   ```
4. During the initial startup, create a superuser account.
   Check your CONTAINER_ID for image named imagelibrary-web
   ```
   $ docker ps
   ```
   Attach to your container
   ```
   $ docker exec -it CONTAINER_ID bash
   ```
   Create superuser account.
   ```
   # python manage.py createsuperuser
   ```
5. Try it on http://localhost:8000 and admin page on http://localhost:8000/admin.

### Production

Uses gunicorn and nginx server.

1. Rename .env.prod.sample to .env
2. Update enviroment variable to fit your needs.
3. Build the images and run containers:
   ```
   $ docker-compose -f docker-compose.prod.yml up -d --build
   ```
4. During the initial startup, create a superuser account.
   Check your CONTAINER_ID for image named imagelibrary-web
   ```
   $ docker ps
   ```
   Attach to your container
   ```
   $ docker exec -it CONTAINER_ID bash
   ```
   Create superuser account.
   ```
   # python manage.py createsuperuser
   ```
5. Try it on http://localhost:1337 and admin page on http://localhost:1337/admin.

## How to use this project?

### Admin

User management.
Every user should have appropriate permissions assigned.

![perms](https://github.com/adrianwo/imagelibrary/assets/5526483/124bd2c6-4d46-413c-a220-f6d0c460745f)

Assign desired values in "User" detail view in section "Profile".

![profile](https://github.com/adrianwo/imagelibrary/assets/5526483/6f2aeb73-daf0-4bb8-b2c9-949510e07760)

