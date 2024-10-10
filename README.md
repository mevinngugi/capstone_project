# Capstone Project - Blog API (High Level Description)
**Description:**
Develop an API for a blogging platform where users can create, update, and delete blog posts, and view posts by category or author.

**Requirements:**
1. CRUD operations for blog posts and users.
2. Endpoint for viewing posts by category or author.
3. Use Django ORM for database interactions.
4. Deploy the API on Heroku or PythonAnywhere.



# BE Capstone Project: Blogging Platform API
### Project Overview:
As a backend developer, your task is to design and implement a **Blogging Platform API** using **Django** and **Django REST Framework**. This API will allow users to manage blog posts by creating, updating, deleting, and viewing posts. You will be responsible for building a fully functional API that interacts with a database to store blog posts and user information, simulating the real-world development of a blogging platform. You will also be tasked with implementing features like categorization and author-based filtering to enhance the blogging experience.

### Functional Requirements:
**1. Blog Post Management (CRUD):**

+ Implement the ability to **Create, Read, Update,** and **Delete** (CRUD) blog posts.
Each blog post should have the following attributes: `Title`, `Content`, `Author`, `Category`, `Published Date`, `Tags` (optional), and `Created Date`.
Ensure validation for required fields like `Title`, `Content`, and `Author`.
Allow each post to be associated with one or more `Tags` (optional, but useful for searching).

**2. Users Management (CRUD):**

+ Implement CRUD operations for users.
A user should have a unique `Username`, `Email`, and `Password`.
Only authenticated users should be able to create, update, or delete their own blog posts.
Implement permission checks to ensure that users can only edit or delete their own posts.

**3. View Posts by Category or Author:**
    
+ Create an endpoint to view posts by **Category**.

Allow users to filter blog posts by `Category` (e.g., Technology, Health, Lifestyle).
+ Create an endpoint to view posts by **Author**.

Users should be able to retrieve all blog posts written by a specific author.
Allow optional filtering by `Published Date` or `Tags` for further refinement.

**4. Search and Filter Blog Posts:**

+ Implement a search feature where users can search for blog posts by `Title`, `Content`, `Tags`, or `Author`.
Add optional filters for `Published Date` or by `Category` to narrow down the results.

### Technical Requirements:
**1. Database:**

+ Use Django ORM to interact with the database.
+ Define models for **Blog Posts**, **Users**, **Categories**, and **Tags**.
+ Ensure each post is associated with an author (user) and can be categorized.

**2. Authentication:**
+ Implement user authentication using **Django’s built-in authentication** system.
+ Users must log in to create, update, or delete blog posts.
+ Optionally, implement token-based authentication (JWT) for additional security.

**3. API Design:**
+ Use **Django Rest Framework** (DRF) to design and expose the necessary API endpoints.
+ Follow RESTful principles: use appropriate HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) for various operations.
+ Ensure proper **error handling**, with appropriate HTTP status codes (e.g., 404 for not found, 400 for bad request).

**4. Deployment:**
+ Deploy the API on **Heroku** or **PythonAnywhere**.
+ Ensure that the API is accessible, secure, and functions well in the deployed environment.

**5. Pagination and Sorting:**
+ Implement pagination for blog post listings to handle large datasets.
+ Provide sorting options, such as sorting by `Published Date` or `Category`.


### Stretch Goals (Optional):
+ **User Comments:** Add a feature allowing users to comment on blog posts, with endpoints to manage (CRUD) comments.
+ **Post Likes and Ratings:** Allow users to like or rate blog posts, and create an endpoint to view the most-liked or highest-rated posts.
+ **Drafts and Publishing:** Implement a feature where users can save blog posts as drafts and publish them later.
+ **Post Sharing:** Create an endpoint that allows users to share blog posts via email or social media platforms.
+ **User Profiles:** Extend the user model to include user profiles where authors can showcase their blog posts, bio, and profile picture.
+ **Subscription System:** Implement a system where users can subscribe to their favorite authors or categories and receive notifications when new posts are published.
+ **Markdown Support:** Add support for Markdown formatting in blog post content to enhance post creation flexibility.